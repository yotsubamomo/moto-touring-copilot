"""M0 LLM Tool Calling Smoke Test and development scenarios (DESIGN.md §9.1, PD-5).

Purpose: check whether a candidate LLM meets the selection criteria with mock
tools, and record model, tokens and estimated cost.

  Smoke cases C1-C3        tool calling: criteria L2-L6
  Development scenarios    D1-D3: multi-step planning (P1), use of tool results
                           (P2), UNKNOWN handling (P3), output correctness (P4)

The development scenarios are independent of the formal E2 question bank and
must never be taken from it.

This is M0 verification code, not product code. All tool outputs are mock data
and carry "simulated": true (NFR5). Nothing here reads GPX or calls CWA.

Modes
  --self-test             Local validation without any API call: a scripted
                          model runs every case (good and deliberately bad
                          behaviours) and the budget guard is exercised.
  --provider anthropic    Real API run against Claude models. Needs the
                          `anthropic` SDK and a credential the SDK can resolve
                          (ANTHROPIC_API_KEY in the environment or the repo-root
                          .env, or an `ant auth login` profile). Without one the
                          run is NOT RUN and no call is made.

Spend control: before every call the worst case is estimated and the call is
refused if it could pass --max-usd; after every call the actual tokens and the
estimated cost are logged and accumulated across the whole multi-turn tool loop.
Costs are estimates (token counts multiplied by PRICES), not an invoice.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_API_URL = "https://api.anthropic.com"

# USD per million tokens (input, output). Standard rates as of 2026-11-03;
# check the current price list before relying on the estimate.
PRICES: dict[str, tuple[float, float]] = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
}

# --------------------------------------------------------------------------
# Mock tools (deterministic, simulated data only)
# --------------------------------------------------------------------------
TOOLS: list[dict[str, Any]] = [
    {
        "name": "find_route",
        "description": "依地名查詢示範路線，回傳 route_id。找不到時 status 為 UNKNOWN。",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "騎士描述的地名或路線名稱"}},
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_eta",
        "description": "計算示範路線終點的典型抵達時間 eta_typ 與保守抵達時間 eta_safe。",
        "input_schema": {
            "type": "object",
            "properties": {
                "route_id": {"type": "string", "pattern": "^R[0-9]{2}$"},
                "departure_time": {
                    "type": "string",
                    "description": "出發時間，ISO 8601，必須帶 +08:00",
                    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?\+08:00$",
                },
            },
            "required": ["route_id", "departure_time"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_weather",
        "description": "查詢抵達時段 [eta_typ, eta_safe] 內的最高降雨機率 pop_max。沒有預報時 status 為 UNKNOWN。",
        "input_schema": {
            "type": "object",
            "properties": {
                "route_id": {"type": "string", "pattern": "^R[0-9]{2}$"},
                "eta_typ": {"type": "string"},
                "eta_safe": {"type": "string"},
            },
            "required": ["route_id", "eta_typ", "eta_safe"],
            "additionalProperties": False,
        },
    },
]
TOOL_SCHEMAS = {t["name"]: t["input_schema"] for t in TOOLS}

_ROUTES = {"武嶺": ("R01", "示範路線甲"), "合歡山": ("R01", "示範路線甲"), "阿里山": ("R02", "示範路線乙")}
_RIDE_MINUTES = {"R01": (310, 350), "R02": (360, 405)}  # (typical, safe)


def _find_route(args: dict) -> dict:
    for key, (rid, name) in _ROUTES.items():
        if key in args["query"]:
            return {"status": "OK", "route_id": rid, "name": name, "simulated": True}
    return {"status": "UNKNOWN", "route_id": None, "reason": "路線不在目錄內", "simulated": True}


def _get_eta(args: dict) -> dict:
    rid = args["route_id"]
    if rid not in _RIDE_MINUTES:
        return {"status": "UNKNOWN", "eta_typ": None, "eta_safe": None, "reason": "沒有這條路線", "simulated": True}
    dep = dt.datetime.fromisoformat(args["departure_time"])
    typ, safe = _RIDE_MINUTES[rid]
    return {
        "status": "OK",
        "route_id": rid,
        "eta_typ": (dep + dt.timedelta(minutes=typ)).isoformat(),
        "eta_safe": (dep + dt.timedelta(minutes=safe)).isoformat(),
        "simulated": True,
    }


def _get_weather(args: dict) -> dict:
    if args["route_id"] == "R01":
        return {"status": "OK", "pop_max": 30, "simulated": True}
    return {"status": "UNKNOWN", "pop_max": None, "reason": "日期超出預報涵蓋期間", "simulated": True}


TOOL_IMPL: dict[str, Callable[[dict], dict]] = {
    "find_route": _find_route,
    "get_eta": _get_eta,
    "get_weather": _get_weather,
}

# --------------------------------------------------------------------------
# Answer formats and cases
# --------------------------------------------------------------------------
_PLAN_PROPS = {
    "route_id": {"type": "string"},
    "departure_time": {"type": ["string", "null"]},
    "eta_typ": {"type": ["string", "null"]},
    "eta_safe": {"type": ["string", "null"]},
    "pop_max": {"type": ["integer", "null"]},
    "weather_status": {"enum": ["OK", "UNKNOWN"]},
    "unknown_items": {"type": "array", "items": {"type": "string"}},
}
PLAN_SCHEMA = {"type": "object", "properties": _PLAN_PROPS, "required": list(_PLAN_PROPS),
               "additionalProperties": False}
_DEV_PROPS = {**_PLAN_PROPS, "plan_status": {"enum": ["FEASIBLE", "CONDITIONAL", "INFEASIBLE"]}}
DEV_PLAN_SCHEMA = {"type": "object", "properties": _DEV_PROPS, "required": list(_DEV_PROPS),
                   "additionalProperties": False}

_COMMON_RULES = (
    "你是重機旅遊規劃助理。所有時間與降雨機率都必須來自工具輸出，不得自行估算。"
    "工具回傳 UNKNOWN 時，對應欄位填 null，並把項目名稱寫進 unknown_items。"
    "時間一律使用帶 +08:00 的 ISO 8601。"
)
SYSTEM_PROMPT = _COMMON_RULES + (
    "完成工具呼叫後，最後只輸出一個 JSON 物件，欄位為："
    "route_id, departure_time, eta_typ, eta_safe, pop_max, weather_status, unknown_items。"
)
DEV_SYSTEM_PROMPT = _COMMON_RULES + (
    "完成工具呼叫後，最後只輸出一個 JSON 物件，欄位為："
    "route_id, departure_time, eta_typ, eta_safe, pop_max, weather_status, unknown_items, plan_status。"
    "plan_status 的規則：有符合期限的出發時間而且天氣查得到，填 FEASIBLE；"
    "有符合期限的出發時間但天氣是 UNKNOWN，填 CONDITIONAL；"
    "沒有任何候選出發時間符合期限，填 INFEASIBLE，這時 departure_time、eta_typ、eta_safe、pop_max 都填 null，"
    "weather_status 填 UNKNOWN，unknown_items 填 [\"weather\"]，不需要查天氣。"
)
_DEV_TASK = (
    "請用工具查出候選出發時間的保守抵達時間 eta_safe，選出 eta_safe 不晚於期限的最晚出發時間，"
    "再查該出發時間抵達時段的降雨機率，最後用指定的 JSON 回答。"
)


@dataclass
class Case:
    case_id: str
    kind: str  # "smoke" or "dev"
    criteria: list[str]
    prompt: str
    expect_route: str
    expect_weather_status: str
    expect_tools: list[str] = field(default_factory=list)       # smoke only
    date: str = ""                                               # dev only below
    candidates: list[str] = field(default_factory=list)
    limit: str = ""
    route_query: str | None = None
    expect_departure: str | None = None
    expect_plan_status: str = ""


CASES = [
    Case("C1", "smoke", ["L2", "L4"],
         "路線 R01，2026-11-21 07:00 出發，請查抵達時間，最後用指定的 JSON 回答。天氣不用查，pop_max 填 null、weather_status 填 UNKNOWN、unknown_items 填 [\"weather\"]。",
         "R01", "UNKNOWN", expect_tools=["get_eta"]),
    Case("C2", "smoke", ["L2", "L3", "L4", "L6"],
         "我想騎武嶺，2026-11-21 早上七點出發，幫我查抵達時間和抵達時段的降雨機率，最後用指定的 JSON 回答。",
         "R01", "OK", expect_tools=["find_route", "get_eta", "get_weather"]),
    Case("C3", "smoke", ["L2", "L3", "L4", "L5", "L6"],
         "我想騎阿里山，2026-11-28 早上六點半出發，幫我查抵達時間和抵達時段的降雨機率，最後用指定的 JSON 回答。",
         "R02", "UNKNOWN", expect_tools=["find_route", "get_eta", "get_weather"]),
]

# Development scenarios. Mock ride times: R01 safe = +5h50m, R02 safe = +6h45m.
DEV_CASES = [
    Case("D1", "dev", ["P1", "P2", "P4"],
         "路線 R01，日期 2026-11-21，最晚 14:00 要抵達終點。候選出發時間只有 07:00、08:00、09:00。" + _DEV_TASK,
         "R01", "OK", date="2026-11-21", candidates=["07:00", "08:00", "09:00"], limit="14:00",
         expect_departure="08:00", expect_plan_status="FEASIBLE"),
    Case("D2", "dev", ["P1", "P2", "P3", "P4"],
         "我想騎阿里山，日期 2026-11-28，最晚 14:00 要抵達終點。候選出發時間只有 06:00、07:00、08:00。" + _DEV_TASK,
         "R02", "UNKNOWN", date="2026-11-28", candidates=["06:00", "07:00", "08:00"], limit="14:00",
         route_query="阿里山", expect_departure="07:00", expect_plan_status="CONDITIONAL"),
    Case("D3", "dev", ["P1", "P2", "P4"],
         "路線 R01，日期 2026-11-21，最晚 12:30 要抵達終點。候選出發時間只有 07:00、08:00、09:00。" + _DEV_TASK,
         "R01", "UNKNOWN", date="2026-11-21", candidates=["07:00", "08:00", "09:00"], limit="12:30",
         expect_departure=None, expect_plan_status="INFEASIBLE"),
]


def _iso(date: str, hhmm: str) -> str:
    return f"{date}T{hhmm}:00+08:00"


def _parse_time(value: Any) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(value) if isinstance(value, str) else None
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Budget guard
# --------------------------------------------------------------------------
class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    cap_usd: float
    price_in_per_mtok: float = 0.0
    price_out_per_mtok: float = 0.0
    spent_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0

    def use_prices(self, price_in_per_mtok: float, price_out_per_mtok: float) -> None:
        self.price_in_per_mtok, self.price_out_per_mtok = price_in_per_mtok, price_out_per_mtok

    def cost(self, tokens_in: int, tokens_out: int) -> float:
        return tokens_in / 1e6 * self.price_in_per_mtok + tokens_out / 1e6 * self.price_out_per_mtok

    def check_next(self, est_tokens_in: int, max_tokens_out: int) -> float:
        """Return the worst-case cost of the next call; refuse it if it could pass the cap."""
        worst = self.cost(est_tokens_in, max_tokens_out)
        if self.spent_usd + worst > self.cap_usd:
            raise BudgetExceeded(f"next call could reach ${self.spent_usd + worst:.4f}, cap is ${self.cap_usd:.2f}")
        return worst

    def add(self, tokens_in: int, tokens_out: int) -> float:
        cost = self.cost(tokens_in, tokens_out)
        self.input_tokens += tokens_in
        self.output_tokens += tokens_out
        self.spent_usd += cost
        return cost


# --------------------------------------------------------------------------
# Model interface
# --------------------------------------------------------------------------
@dataclass
class ModelTurn:
    tool_calls: list[dict] = field(default_factory=list)  # {"id", "name", "arguments"}
    text: str | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    stop_reason: str | None = None


class ScriptedModel:
    """Stands in for an LLM during local validation. No network access.

    behaviour: good | wrong_tool | bad_args | skip_chain | bad_json | fabricate
               | pick_first | wrong_status   (the last two apply to dev scenarios)
    """

    model_id = "scripted-local"
    max_tokens_out = 800

    def __init__(self, behaviour: str = "good"):
        self.behaviour = behaviour

    def step(self, system: str, messages: list[dict], tools: list[dict], case: Case) -> ModelTurn:
        usage = dict(tokens_in=400 + 150 * len(messages), tokens_out=80)
        results = [m for m in messages if m["role"] == "tool"]
        if case.kind == "dev":
            return self._step_dev(results, case, usage)
        return self._step_smoke(results, case, usage)

    def _step_smoke(self, results: list[dict], case: Case, usage: dict) -> ModelTurn:
        done = [m["name"] for m in results]
        last = {m["name"]: m["content"] for m in results}
        dep = "2026-11-21T07:00:00+08:00" if case.case_id != "C3" else "2026-11-28T06:30:00+08:00"

        for name in case.expect_tools:
            if name in done:
                continue
            if name == "find_route":
                key = "武嶺" if case.expect_route == "R01" else "阿里山"
                return ModelTurn([{"id": "c1", "name": "find_route", "arguments": {"query": key}}], **usage)
            if name == "get_eta":
                rid = last["find_route"]["route_id"] if "find_route" in last else case.expect_route
                tool = "get_weather" if self.behaviour == "wrong_tool" else "get_eta"
                args: dict = {"route_id": rid, "departure_time": dep}
                if self.behaviour == "bad_args":
                    args = {"route_id": rid, "departure_time": "2026-11-21 07:00"}  # no offset
                if tool == "get_weather":
                    args = {"route_id": rid, "eta_typ": dep, "eta_safe": dep}
                return ModelTurn([{"id": "c2", "name": tool, "arguments": args}], **usage)
            if name == "get_weather":
                eta = last["get_eta"]
                typ = dep if self.behaviour == "skip_chain" else eta["eta_typ"]
                return ModelTurn([{"id": "c3", "name": "get_weather",
                                   "arguments": {"route_id": eta.get("route_id"), "eta_typ": typ,
                                                 "eta_safe": eta.get("eta_safe")}}], **usage)

        eta = last.get("get_eta", {})
        weather = last.get("get_weather", {"status": "UNKNOWN", "pop_max": None})
        weather_ok = weather.get("status") == "OK"
        plan = {
            "route_id": eta.get("route_id"), "departure_time": dep,
            "eta_typ": eta.get("eta_typ"), "eta_safe": eta.get("eta_safe"),
            "pop_max": weather.get("pop_max") if weather_ok else None,
            "weather_status": "OK" if weather_ok else "UNKNOWN",
            "unknown_items": [] if weather_ok else ["weather"],
        }
        if self.behaviour == "fabricate" and not weather_ok:
            plan.update(pop_max=20, weather_status="OK", unknown_items=[])
        text = json.dumps(plan, ensure_ascii=False)
        if self.behaviour == "bad_json":
            text = "建議 07:00 出發，預計下午抵達。"
        return ModelTurn(text=text, **usage)

    def _step_dev(self, results: list[dict], case: Case, usage: dict) -> ModelTurn:
        route = next((m["content"].get("route_id") for m in results if m["name"] == "find_route"), None)
        if case.route_query and route is None:
            return ModelTurn([{"id": "d0", "name": "find_route", "arguments": {"query": case.route_query}}], **usage)
        rid = route or case.expect_route
        deps = [_iso(case.date, c) for c in case.candidates]
        etas = {m["arguments"]["departure_time"]: m["content"] for m in results if m["name"] == "get_eta"}
        if not etas:  # ask for every candidate in one turn (parallel tool calls)
            return ModelTurn([{"id": f"d{i + 1}", "name": "get_eta", "arguments": {"route_id": rid, "departure_time": d}}
                              for i, d in enumerate(deps)], **usage)

        limit = _parse_time(_iso(case.date, case.limit))
        feasible = [d for d in deps if _parse_time(etas[d]["eta_safe"]) <= limit]
        chosen = None
        if feasible:
            chosen = min(feasible) if self.behaviour == "pick_first" else max(feasible)
        elif self.behaviour == "wrong_status":
            chosen = deps[0]  # claims a plan although no candidate meets the limit

        weather = next((m["content"] for m in results if m["name"] == "get_weather"), None)
        if chosen and weather is None:
            return ModelTurn([{"id": "d9", "name": "get_weather",
                               "arguments": {"route_id": rid, "eta_typ": etas[chosen]["eta_typ"],
                                             "eta_safe": etas[chosen]["eta_safe"]}}], **usage)
        if chosen is None:
            plan = {"route_id": rid, "departure_time": None, "eta_typ": None, "eta_safe": None, "pop_max": None,
                    "weather_status": "UNKNOWN", "unknown_items": ["weather"], "plan_status": "INFEASIBLE"}
        else:
            weather_ok = weather.get("status") == "OK"
            plan = {"route_id": rid, "departure_time": chosen,
                    "eta_typ": etas[chosen]["eta_typ"], "eta_safe": etas[chosen]["eta_safe"],
                    "pop_max": weather.get("pop_max") if weather_ok else None,
                    "weather_status": "OK" if weather_ok else "UNKNOWN",
                    "unknown_items": [] if weather_ok else ["weather"],
                    "plan_status": "FEASIBLE" if weather_ok else "CONDITIONAL"}
            if self.behaviour == "fabricate" and not weather_ok:
                plan.update(pop_max=20, weather_status="OK", unknown_items=[], plan_status="FEASIBLE")
        return ModelTurn(text=json.dumps(plan, ensure_ascii=False), **usage)


class AnthropicModel:
    """Claude through the official Anthropic SDK, with a manual tool loop.

    The loop is manual because the harness has to record and check every tool
    call. Thinking is left at the model default (adaptive). Sampling parameters
    are not sent: current Claude models reject non-default values, so the
    settings that can be pinned for a fair comparison are the model ID, the
    effort level and max_tokens.

    The client is pinned to the official endpoint, so an ANTHROPIC_BASE_URL in
    the environment cannot redirect the credential elsewhere.

    Refusal fallbacks are deliberately not enabled: a fallback would let a
    different model answer, and this test measures one named model. A refusal
    is recorded as a failed run.
    """

    def __init__(self, model_id: str, effort: str, max_tokens_out: int):
        import anthropic  # imported here so --self-test works without the SDK

        # An explicit base_url wins over ANTHROPIC_BASE_URL and over a profile's own base URL,
        # for API keys and for `ant auth login` profiles alike.
        self.client = anthropic.Anthropic(base_url=ALLOWED_API_URL)
        if self.client.base_url.host != urlparse(ALLOWED_API_URL).hostname:
            raise RuntimeError("client endpoint is not the official API host")
        self.model_id = model_id
        self.effort = effort
        self.max_tokens_out = max_tokens_out
        self._native: list[dict] = []

    def step(self, system: str, messages: list[dict], tools: list[dict], case: Case) -> ModelTurn:
        if len(messages) == 1:  # a new case starts
            self._native = [{"role": "user", "content": messages[0]["content"]}]
        else:
            pending = []
            for m in reversed(messages):
                if m["role"] != "tool":
                    break
                pending.append(m)
            results = []
            for m in reversed(pending):
                block = {"type": "tool_result", "tool_use_id": m["tool_call_id"],
                         "content": json.dumps(m["content"], ensure_ascii=False)}
                if m["content"].get("status") == "ERROR":
                    block["is_error"] = True
                results.append(block)
            # all tool results for one assistant turn go back in a single user message
            self._native.append({"role": "user", "content": results})

        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=self.max_tokens_out,
            system=system,
            tools=tools,
            messages=self._native,
            output_config={"effort": self.effort},
        )
        # keep the full content (thinking and tool_use blocks) for the next request
        self._native.append({"role": "assistant", "content": response.content})

        usage = response.usage
        tokens_in = (usage.input_tokens or 0) + (getattr(usage, "cache_creation_input_tokens", 0) or 0) \
            + (getattr(usage, "cache_read_input_tokens", 0) or 0)
        turn = ModelTurn(tokens_in=tokens_in, tokens_out=usage.output_tokens or 0, stop_reason=response.stop_reason)
        if response.stop_reason == "tool_use":
            turn.tool_calls = [{"id": b.id, "name": b.name, "arguments": b.input}
                               for b in response.content if b.type == "tool_use"]
        turn.text = "".join(b.text for b in response.content if b.type == "text") or None
        return turn


# --------------------------------------------------------------------------
# Harness and checks
# --------------------------------------------------------------------------
def run_case(model, case: Case, budget: Budget | None, max_steps: int = 10) -> dict:
    system = DEV_SYSTEM_PROMPT if case.kind == "dev" else SYSTEM_PROMPT
    messages: list[dict] = [{"role": "user", "content": case.prompt}]
    calls: list[dict] = []
    call_log: list[dict] = []
    final_text, stop_reasons = None, []
    tokens = [0, 0]
    for step in range(1, max_steps + 1):
        entry: dict[str, Any] = {"step": step}
        if budget is not None:
            # characters as a high estimate of input tokens, plus the tool definitions
            est_in = 1500 + sum(len(json.dumps(m, ensure_ascii=False, default=str)) for m in messages)
            entry["est_worst_usd"] = round(budget.check_next(est_in, model.max_tokens_out), 6)
        turn = model.step(system, messages, TOOLS, case)
        tokens[0] += turn.tokens_in
        tokens[1] += turn.tokens_out
        stop_reasons.append(turn.stop_reason)
        entry.update(tokens_in=turn.tokens_in, tokens_out=turn.tokens_out, stop_reason=turn.stop_reason)
        if budget is not None:
            entry["cost_usd"] = round(budget.add(turn.tokens_in, turn.tokens_out), 6)
            entry["cumulative_usd"] = round(budget.spent_usd, 6)
        call_log.append(entry)
        if not turn.tool_calls:
            final_text = turn.text
            break
        messages.append({"role": "assistant", "tool_calls": turn.tool_calls, "content": turn.text})
        for call in turn.tool_calls:
            record = {"name": call["name"], "arguments": call["arguments"], "schema_valid": True, "error": None}
            try:
                jsonschema.validate(call["arguments"], TOOL_SCHEMAS[call["name"]])
                output = TOOL_IMPL[call["name"]](call["arguments"])
            except (jsonschema.ValidationError, KeyError) as exc:
                record.update(schema_valid=False, error=str(exc).splitlines()[0])
                output = {"status": "ERROR", "reason": "invalid tool call"}
            record["output"] = output
            calls.append(record)
            messages.append({"role": "tool", "tool_call_id": call["id"], "name": call["name"],
                             "arguments": call["arguments"], "content": output})
    checker = check_dev_case if case.kind == "dev" else check_case
    return {"case_id": case.case_id, "kind": case.kind, "calls": calls, "final_text": final_text,
            "stop_reasons": stop_reasons, "truncated": "max_tokens" in stop_reasons,
            "tokens_in": tokens[0], "tokens_out": tokens[1], "call_log": call_log,
            "checks": checker(case, calls, final_text)}


def _parse_plan(text: str | None, schema: dict) -> dict | None:
    """Return the plan object if the text holds one that matches the schema."""
    if not text:
        return None
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        plan = json.loads(text[start:end + 1])
        jsonschema.validate(plan, schema)
    except (json.JSONDecodeError, jsonschema.ValidationError):
        return None
    return plan


def check_case(case: Case, calls: list[dict], final_text: str | None) -> dict[str, bool]:
    """Smoke cases. Each key is a selection criterion from DESIGN.md §9.1."""
    names = [c["name"] for c in calls]
    by_name = {c["name"]: c for c in calls}
    checks: dict[str, bool] = {}
    plan = _parse_plan(final_text, PLAN_SCHEMA)

    # L2: the expected tools, in order, with schema-valid arguments
    checks["L2"] = names == case.expect_tools and all(c["schema_valid"] for c in calls)

    # L3: the later call uses the earlier tool's output
    if "L3" in case.criteria:
        ok = {"find_route", "get_eta", "get_weather"} <= set(by_name)
        if ok:
            ok = (by_name["get_eta"]["arguments"].get("route_id") == by_name["find_route"]["output"].get("route_id")
                  and by_name["get_weather"]["arguments"].get("eta_typ") == by_name["get_eta"]["output"].get("eta_typ")
                  and by_name["get_weather"]["arguments"].get("eta_safe") == by_name["get_eta"]["output"].get("eta_safe"))
        checks["L3"] = bool(ok)

    # L4: final answer matches the plan format and repeats the tool numbers exactly
    if "L4" in case.criteria:
        ok = plan is not None and "get_eta" in by_name
        if ok:
            eta = by_name["get_eta"]["output"]
            ok = (plan["route_id"] == case.expect_route and plan["eta_typ"] == eta.get("eta_typ")
                  and plan["eta_safe"] == eta.get("eta_safe") and plan["weather_status"] == case.expect_weather_status)
            if ok and case.expect_weather_status == "OK":
                ok = plan["pop_max"] == by_name["get_weather"]["output"]["pop_max"]
        checks["L4"] = bool(ok)

    # L5: UNKNOWN from a tool is reported as UNKNOWN, with no invented value
    if "L5" in case.criteria:
        checks["L5"] = bool(plan is not None and plan["pop_max"] is None and plan["weather_status"] == "UNKNOWN"
                            and len(plan["unknown_items"]) > 0)

    # L6: Traditional Chinese place name resolved to the right route
    if "L6" in case.criteria:
        checks["L6"] = bool("find_route" in by_name and by_name["find_route"]["output"].get("route_id") == case.expect_route
                            and plan is not None and plan["route_id"] == case.expect_route)
    return checks


def check_dev_case(case: Case, calls: list[dict], final_text: str | None) -> dict[str, bool]:
    """Development scenarios: P1 planning, P2 tool-result use, P3 UNKNOWN handling, P4 output."""
    plan = _parse_plan(final_text, DEV_PLAN_SCHEMA)
    eta_by_dep = {_parse_time(c["arguments"].get("departure_time")): c["output"]
                  for c in calls if c["name"] == "get_eta" and c["schema_valid"]}
    weather_calls = [c for c in calls if c["name"] == "get_weather" and c["schema_valid"]]
    deps = [_parse_time(_iso(case.date, c)) for c in case.candidates]
    expected = _parse_time(_iso(case.date, case.expect_departure)) if case.expect_departure else None
    # to justify "the latest feasible departure" the model must have looked at it and at every later candidate
    needed = deps if expected is None else [d for d in deps if d >= expected]
    checks: dict[str, bool] = {}

    checks["P1"] = bool(all(c["schema_valid"] for c in calls) and all(d in eta_by_dep for d in needed)
                        and plan is not None and _parse_time(plan["departure_time"]) == expected)

    if expected is None:
        checks["P2"] = bool(plan is not None and plan["eta_typ"] is None and plan["eta_safe"] is None)
    else:
        eta = eta_by_dep.get(expected, {})
        ok = (plan is not None and plan["eta_typ"] == eta.get("eta_typ") and plan["eta_safe"] == eta.get("eta_safe"))
        ok = ok and any(w["arguments"].get("eta_typ") == eta.get("eta_typ")
                        and w["arguments"].get("eta_safe") == eta.get("eta_safe") for w in weather_calls)
        if ok and case.expect_weather_status == "OK":
            ok = plan["pop_max"] == weather_calls[-1]["output"].get("pop_max")
        checks["P2"] = bool(ok)

    if "P3" in case.criteria:
        checks["P3"] = bool(plan is not None and plan["pop_max"] is None and plan["weather_status"] == "UNKNOWN"
                            and len(plan["unknown_items"]) > 0 and plan["plan_status"] == "CONDITIONAL")

    checks["P4"] = bool(plan is not None and plan["plan_status"] == case.expect_plan_status
                        and plan["route_id"] == case.expect_route)
    return checks


def summarise(results: list[dict]) -> dict[str, str]:
    summary: dict[str, list[bool]] = {}
    for r in results:
        for key, ok in r["checks"].items():
            summary.setdefault(key, []).append(ok)
    return {k: f"{sum(v)}/{len(v)}" for k, v in sorted(summary.items())}


# --------------------------------------------------------------------------
# Local validation
# --------------------------------------------------------------------------
def self_test() -> dict:
    report: dict[str, Any] = {"mode": "local-scripted", "api_calls": 0, "spent_usd": 0.0}
    all_cases = CASES + DEV_CASES
    by_id = {c.case_id: c for c in all_cases}

    good = [run_case(ScriptedModel("good"), c, None) for c in all_cases]
    report["good_model"] = {"smoke": summarise([r for r in good if r["kind"] == "smoke"]),
                            "dev": summarise([r for r in good if r["kind"] == "dev"]),
                            "all_pass": all(all(r["checks"].values()) for r in good)}

    # Each bad behaviour must be caught by the criterion it violates.
    expected_failures = [
        ("wrong_tool", "C1", "L2"),
        ("bad_args", "C1", "L2"),
        ("skip_chain", "C2", "L3"),
        ("bad_json", "C2", "L4"),
        ("fabricate", "C3", "L5"),
        ("pick_first", "D1", "P1"),
        ("fabricate", "D2", "P3"),
        ("wrong_status", "D3", "P4"),
    ]
    detection = {}
    for behaviour, case_id, criterion in expected_failures:
        result = run_case(ScriptedModel(behaviour), by_id[case_id], None)
        detection[f"{behaviour}@{case_id}"] = {"criterion": criterion,
                                               "detected": result["checks"].get(criterion) is False}
    report["bad_model_detection"] = detection

    # Budget guard: must stop before the cap, count spend correctly and log every call.
    budget = Budget(cap_usd=0.10, price_in_per_mtok=3.0, price_out_per_mtok=15.0)
    stopped, completed, logged, last = False, 0, 0, None
    try:
        for _ in range(50):
            for case in all_cases:
                last = run_case(ScriptedModel("good"), case, budget)
                completed += 1
                logged += len(last["call_log"])
    except BudgetExceeded:
        stopped = True
    expected_cost = budget.input_tokens / 1e6 * 3.0 + budget.output_tokens / 1e6 * 15.0
    log_ok = last is not None and all({"est_worst_usd", "tokens_in", "tokens_out", "cost_usd", "cumulative_usd"} <= set(e)
                                       for e in last["call_log"])
    report["budget_guard"] = {"stopped_before_cap": stopped and completed > 0 and budget.spent_usd <= budget.cap_usd,
                              "spend_matches_tokens": budget.spent_usd > 0 and abs(budget.spent_usd - expected_cost) < 1e-12,
                              "per_call_log_complete": log_ok,
                              "cases_completed_before_stop": completed, "calls_logged": logged,
                              "fake_spend_usd": round(budget.spent_usd, 6), "fake_cap_usd": budget.cap_usd,
                              "note": "fake prices and scripted token counts; not a real cost"}

    report["passed"] = (report["good_model"]["all_pass"]
                        and all(d["detected"] for d in detection.values())
                        and all(v for k, v in report["budget_guard"].items()
                                if k in ("stopped_before_cap", "spend_matches_tokens", "per_call_log_complete")))
    return report


# --------------------------------------------------------------------------
# Real API run
# --------------------------------------------------------------------------
def _load_dotenv() -> None:
    """Read ANTHROPIC_API_KEY from the repo-root .env if it is not already set. Never printed."""
    env_file = REPO_ROOT / ".env"
    if "ANTHROPIC_API_KEY" in os.environ or not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key.strip() == "ANTHROPIC_API_KEY" and value.strip():
            os.environ["ANTHROPIC_API_KEY"] = value.strip().strip('"').strip("'")


def _profile_config_dir() -> Path:
    """Where the SDK looks for `ant auth login` profiles (same rule as the SDK's credential chain)."""
    override = os.environ.get("ANTHROPIC_CONFIG_DIR")
    if override:
        return Path(override)
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        return (Path(appdata) if appdata else Path.home() / "AppData" / "Roaming") / "Anthropic"
    return Path.home() / ".config" / "anthropic"


def _has_credential() -> bool:
    """True if the SDK has something to resolve. Checks presence only; no credential is read here.

    Supported, in the SDK's own order: ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, a profile named by
    ANTHROPIC_PROFILE, workload identity variables, or the profile written by `ant auth login`.
    The SDK does the actual resolution when the client is built.
    """
    env = os.environ
    if env.get("ANTHROPIC_API_KEY") or env.get("ANTHROPIC_AUTH_TOKEN") or env.get("ANTHROPIC_PROFILE"):
        return True
    if env.get("ANTHROPIC_FEDERATION_RULE_ID") and env.get("ANTHROPIC_ORGANIZATION_ID"):
        return True
    configs = _profile_config_dir() / "configs"
    return configs.is_dir() and any(configs.glob("*.json"))


def check_endpoint() -> str | None:
    """Return a reason to refuse the run if ANTHROPIC_BASE_URL is not the official endpoint.

    Only the scheme and host are reported, never the full value.
    """
    raw = os.environ.get("ANTHROPIC_BASE_URL")
    if not raw:
        return None
    parsed, allowed = urlparse(raw), urlparse(ALLOWED_API_URL)
    if parsed.scheme != allowed.scheme or parsed.hostname != allowed.hostname or parsed.port not in (None, 443):
        return (f"ANTHROPIC_BASE_URL points to {parsed.scheme}://{parsed.hostname}, "
                f"which is not {ALLOWED_API_URL}. The credential is not sent there.")
    return None


def _test_model(model_id: str, repeats: int, budget: Budget, effort: str, max_tokens_out: int) -> dict:
    import anthropic

    budget.use_prices(*PRICES[model_id])
    spent_before, tok_before = budget.spent_usd, (budget.input_tokens, budget.output_tokens)
    cases = CASES + DEV_CASES
    runs: list[dict] = []
    error = None
    try:
        model = AnthropicModel(model_id, effort, max_tokens_out)
        for repeat in range(repeats):
            for case in cases:
                result = run_case(model, case, budget)
                result["repeat"] = repeat + 1
                runs.append(result)
    except BudgetExceeded as exc:
        error = f"budget: {exc}"
    except anthropic.AuthenticationError:
        error = "authentication failed: the credential was rejected"
    except anthropic.PermissionDeniedError:
        error = "permission denied for this model or credential"
    except anthropic.NotFoundError:
        error = "model not found for this account"
    except anthropic.RateLimitError:
        error = "rate limited after SDK retries"
    except anthropic.APIStatusError as exc:
        error = f"API error {exc.status_code}: {exc.message}"
    except anthropic.APIConnectionError:
        error = "network error"
    except (anthropic.AnthropicError, TypeError, RuntimeError) as exc:
        # e.g. a profile that cannot be loaded, or no usable credential. Only the error type is
        # recorded, so nothing from a credential file can end up in the report.
        error = f"credential: could not be resolved or used ({type(exc).__name__})"

    smoke = [r for r in runs if r["kind"] == "smoke"]
    dev = [r for r in runs if r["kind"] == "dev"]
    complete = error is None and len(runs) == repeats * len(cases)
    cost = budget.spent_usd - spent_before
    return {
        "smoke": summarise(smoke), "dev": summarise(dev),
        "runs_completed": len(runs), "runs_planned": repeats * len(cases),
        "smoke_all_pass": complete and all(all(r["checks"].values()) for r in smoke),
        "dev_all_pass": complete and all(all(r["checks"].values()) for r in dev),
        "meets_bar": complete and all(all(r["checks"].values()) for r in runs),
        "truncated_runs": sum(r["truncated"] for r in runs),
        "error": error,
        "input_tokens": budget.input_tokens - tok_before[0], "output_tokens": budget.output_tokens - tok_before[1],
        "estimated_cost_usd": round(cost, 6),
        "avg_cost_per_case_usd": round(cost / len(runs), 6) if runs else None,
        "runs": runs,
    }


def real_run(models: list[str], repeats: int, cap_usd: float, effort: str, max_tokens_out: int,
             test_all: bool) -> dict:
    """Candidates are ordered cheapest first. The first two are always tested;
    later ones only if no earlier candidate met the bar (or with test_all)."""
    import anthropic

    report: dict[str, Any] = {"mode": "real-api", "provider": "anthropic", "sdk_version": anthropic.__version__,
                              "endpoint": ALLOWED_API_URL, "cap_usd": cap_usd, "effort": effort,
                              "max_tokens": max_tokens_out, "repeats": repeats, "models": {}, "not_tested": {},
                              "stopped_reason": None,
                              "price_note": "estimated from token counts and PRICES; not an invoice"}
    budget = Budget(cap_usd=cap_usd)
    for index, model_id in enumerate(models):
        met = [m for m, r in report["models"].items() if r["meets_bar"]]
        if index >= 2 and met and not test_all:
            report["not_tested"][model_id] = f"not needed: {', '.join(met)} met the bar"
            continue
        result = _test_model(model_id, repeats, budget, effort, max_tokens_out)
        report["models"][model_id] = result
        if result["error"] and result["error"].startswith(("budget", "authentication", "credential")):
            report["stopped_reason"] = result["error"]
            for rest in models[index + 1:]:
                report["not_tested"][rest] = "run stopped early"
            break
    report["total_input_tokens"], report["total_output_tokens"] = budget.input_tokens, budget.output_tokens
    report["spent_usd"] = round(budget.spent_usd, 6)
    return report


def _emit(report: dict, out: Path | None) -> None:
    report["run_at"] = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    text = json.dumps(report, ensure_ascii=False, indent=2, default=str)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true", help="local validation, no API call")
    parser.add_argument("--provider", choices=["anthropic"], help="run against a real API")
    parser.add_argument("--models", default="claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5",
                        help="comma-separated candidates; run cheapest first, the first two always")
    parser.add_argument("--repeats", type=int, default=3, help="times each case is run per model")
    parser.add_argument("--max-usd", type=float, help="hard spend cap for this run (required for a real run)")
    parser.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="raise only on evidence of truncation (truncated_runs in the report)")
    parser.add_argument("--test-all", action="store_true",
                        help="test every candidate even when a cheaper one already met the bar")
    parser.add_argument("--out", type=Path, help="write the JSON report to this file")
    args = parser.parse_args()

    if args.self_test:
        report = self_test()
        _emit(report, args.out)
        return 0 if report["passed"] else 1

    if args.provider == "anthropic":
        if args.max_usd is None:
            parser.error("--max-usd is required for a real API run")
        models = [m.strip() for m in args.models.split(",") if m.strip()]
        unknown = [m for m in models if m not in PRICES]
        if unknown:
            parser.error(f"no price listed for: {', '.join(unknown)}")
        models.sort(key=lambda m: PRICES[m][1])
        refusal = check_endpoint()
        if refusal:
            print(f"NOT RUN. {refusal} No API call was made.", file=sys.stderr)
            return 4
        _load_dotenv()
        if not _has_credential():
            print("NOT RUN. No Anthropic credential found (ANTHROPIC_API_KEY in the environment or the repo-root "
                  ".env, or an `ant auth login` profile). No API call was made.", file=sys.stderr)
            return 3
        report = real_run(models, args.repeats, args.max_usd, args.effort, args.max_tokens, args.test_all)
        _emit(report, args.out)
        return 0 if any(m["meets_bar"] for m in report["models"].values()) else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
