"""UI-0 Streamlit mock-data skeleton (GitHub Issue #12, SPEC-UI0).

Run from the repository root:

    .venv/Scripts/python.exe -m streamlit run app/ui0_mock_app.py

Everything on screen is synthetic mock data and is labelled as such. The app
does not import ``src/moto_copilot`` (CL-UI0-1), does not read ``data/``, does
not call any routing engine, language model or other API, and does not compute
any rule result or plan status: those are literal values in ``ui0_scenarios``
(CL-UI0-5).

Uploaded files are never read, parsed, written to disk or logged; only the
number of selected files is used (CL-UI0-2). The Streamlit uploader widget
itself shows the file names and sizes.
"""

from __future__ import annotations

import datetime as dt

import streamlit as st

import ui0_scenarios as S
import ui0_texts as T
from ui0_guard import guard_hits


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

FORM_FIELDS = ("desc", "trip", "date", "earliest", "deadline", "fuel", "gpx", "snapshot")
FIELD_LABEL = {
    "desc": "行程描述",
    "trip": "行程型態",
    "date": "日期",
    "earliest": "最早可出發時間",
    "deadline": "期限",
    "fuel": "出發油量",
    "gpx": "目標路線 GPX 的檔案路徑",
    "snapshot": "Snapshot Mode",
}

ss = st.session_state


def current_scenario() -> dict:
    return S.SCENARIO_BY_ID[ss["scenario"]]


def fkey(name: str) -> str:
    """Widget key of a form field. A new scenario gets new keys, so the widgets start
    from the scenario's values (``value=``) without writing to widget state."""
    return f"f_{name}_{ss['nonce']}"


def read_inputs() -> dict:
    defaults = current_scenario()["form"]
    return {name: ss.get(fkey(name), defaults[name]) for name in FORM_FIELDS}


def apply_scenario() -> None:
    """Reset everything to the selected scenario (callback of the scenario menu)."""
    scenario = current_scenario()
    ss["nonce"] = ss.get("nonce", 0) + 1
    ss["profile_id"] = scenario["profile"]
    ss["profile_result"] = None
    ss["profile_steps_shown"] = False
    ss["field_errors"] = {}
    ss["clarify_answers"] = None
    ss["stale_profile"] = False
    if scenario.get("preplanned"):
        ss["outcome"] = dict(scenario["outcome"])
        ss["plan_inputs"] = dict(scenario["form"])
        ss["plan_steps"] = "complete"
    else:
        ss["outcome"] = None
        ss["plan_inputs"] = None
        ss["plan_steps"] = None


def on_update_profile() -> None:
    files = ss.get(f"uploads_{ss['nonce']}") or []
    if not files:
        ss["profile_result"] = {"none_selected": True}
        ss["profile_steps_shown"] = False
        return
    # Only the count is used. The files are not read (CL-UI0-2).
    ss["profile_result"] = {"selected": len(files), **S.PROFILE_UPDATE_RESULT}
    ss["profile_steps_shown"] = True
    ss["profile_id"] = current_scenario()["profile_after"]
    if ss.get("outcome") is not None:
        ss["stale_profile"] = True


def on_plan() -> None:
    inputs = read_inputs()
    errors: dict[str, str] = {}
    desc = (inputs["desc"] or "").strip()
    gpx = (inputs["gpx"] or "").strip()
    if not desc and not gpx:
        errors["desc"] = T.FIELD_ERROR_NO_ROUTE_INPUT
    elif desc and guard_hits(desc):
        errors["desc"] = T.GUARD_MESSAGE
    if inputs["fuel"] is None:
        errors["fuel"] = T.FIELD_ERROR_FUEL
    ss["field_errors"] = errors
    if errors:
        return  # Not submitted; an earlier result (if any) stays and is checked for staleness.

    outcome = dict(current_scenario()["outcome"])
    ss["clarify_answers"] = None
    ss["stale_profile"] = False
    ss["plan_inputs"] = inputs
    if outcome["kind"] == "rest_unmapped":
        ss["field_errors"] = {"desc": T.fill(T.REST_STILL_UNMAPPED, 休息需求的原文=outcome["source_text"])}
        ss["outcome"] = None
        ss["plan_steps"] = None
        ss["plan_inputs"] = None
        return
    ss["outcome"] = outcome
    ss["plan_steps"] = {
        "plan": "complete",
        "clarify": "clarify",
        "route_error": "route_error",
        "evaluation_failed": "evaluation_failed",
        "profile_only": None,
    }[outcome["kind"]]


def needed_questions(questions: list[dict], answers: dict) -> list[dict]:
    """Questions that must be answered: the 'only if round trip' direction is skipped for 單向."""
    needed = []
    for question in questions:
        if question["kind"] == "direction_if_round" and answers.get("trip") == T.TRIP_ONE_WAY:
            continue
        needed.append(question)
    return needed


def on_clarify_reply() -> None:
    outcome = ss["outcome"]
    questions = outcome["questions"]
    answers = {q["id"]: ss.get(f"clarify_{q['id']}") for q in questions}
    if any(answers[q["id"]] is None for q in needed_questions(questions, answers)):
        ss["clarify_error"] = True
        return
    ss["clarify_error"] = False
    ss["clarify_answers"] = answers
    trip = answers.get("trip") or read_inputs()["trip"]
    plan = "round" if trip == T.TRIP_ROUND else "one_way"
    ss["outcome"] = {"kind": "plan", "plan": plan, "after_clarify": outcome["questions"]}
    ss["plan_steps"] = "complete"


def init_state() -> None:
    if "scenario" not in ss:
        ss["scenario"] = S.SCENARIOS[0]["id"]
        apply_scenario()


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def badge(spec: tuple[str, str, str]) -> None:
    label, color, icon = spec
    st.badge(label, color=color, icon=icon)


def mock_badge() -> None:
    st.badge("模擬", color="violet", icon=":material/science:")


def deadline_label(trip: str | None) -> str:
    if trip == T.TRIP_ROUND:
        return T.DEADLINE_ROUND
    if trip == T.TRIP_ONE_WAY:
        return T.DEADLINE_ONE_WAY
    return T.DEADLINE_FIXED


def render_header() -> None:
    st.title("Moto Touring Copilot 重機旅遊規劃顧問")
    st.caption("出發前的決策輔助：最晚幾點出發還來得及？（UI-0 Mock-data Skeleton）")
    with st.container(horizontal=True):
        st.badge("模擬資料：本頁不連接任何 API 或語言模型", color="violet", icon=":material/science:")
        outcome = ss.get("outcome")
        if outcome is not None and ss.get("plan_inputs"):
            if ss["plan_inputs"].get("snapshot"):
                st.badge("Snapshot Mode：目前顯示的結果使用固定的資料快照", color="blue", icon=":material/info:")
        elif read_inputs()["snapshot"]:
            st.badge("Snapshot Mode：下次規劃會使用固定的資料快照", color="blue", icon=":material/info:")


def render_controls() -> None:
    with st.container(border=True):
        st.subheader("Skeleton 控制（不屬於產品畫面）")
        st.caption("用來切換模擬情境。切換時表單、Profile 與結果都重設為該情境的模擬資料。")
        st.selectbox(
            "模擬情境",
            [s["id"] for s in S.SCENARIOS],
            format_func=lambda sid: S.SCENARIO_BY_ID[sid]["label"],
            key="scenario",
            on_change=apply_scenario,
        )
        st.caption("模擬：" + current_scenario()["note"])


def render_profile() -> None:
    profile = S.PROFILES[ss["profile_id"]]
    with st.expander("Profile：歷史 GPX 與涵蓋度摘要", expanded=False):
        st.caption(T.PROFILE_PRIVACY)
        st.file_uploader(
            "選取歷史 GPX（可以一次選取多個 .gpx 檔）",
            type=["gpx"],
            accept_multiple_files=True,
            key=f"uploads_{ss['nonce']}",
        )
        st.button("更新 Profile", key="update_profile", on_click=on_update_profile)
        result = ss.get("profile_result")
        if result and result.get("none_selected"):
            st.warning(T.UPLOAD_NONE_SELECTED)
        elif result:
            unreadable = "；".join(f"{count}無法讀取（原因：{reason}）" for count, reason in result["unreadable"])
            st.info(
                f"處理結果（模擬，與選取的 {result['selected']} 個檔案的內容無關）："
                f"新增 {result['added']} 個；略過 {result['duplicates']} 個內容重複的；{unreadable}。"
            )
        with st.container(horizontal=True):
            st.markdown("**涵蓋度摘要**")
            mock_badge()
        cols = st.columns(3)
        cols[0].metric("可用的行程數", profile["trips"])
        cols[1].metric("可用的路段數", profile["segments"])
        cols[2].metric("累計公里", profile["km"])
        st.table(profile["rows"], hide_index=True)
        for kind, text in profile["notes"]:
            (st.warning if kind == "warning" else st.info)(text)
    if ss.get("profile_steps_shown"):
        with st.status("Profile 更新完成（模擬）", state="complete", expanded=False):
            for step in S.PROFILE_UPDATE_STEPS:
                st.write(f"{step}：完成")


def render_planner() -> None:
    st.header("Trip Planner")
    errors = ss.get("field_errors") or {}
    form = current_scenario()["form"]
    trip_options = [T.TRIP_ROUND, T.TRIP_ONE_WAY]
    st.text_area(
        "行程描述（起點、目的地或公路、途經點、來回或單向、休息與偏好）",
        value=form["desc"],
        key=fkey("desc"),
        height=100,
    )
    st.caption(T.DESC_CAPTION)
    if "desc" in errors:
        st.error(errors["desc"])
    with st.expander("可用的公路與地標（模擬）"):
        st.table(S.GAZETTEER, hide_index=True)
    st.radio(
        "行程型態（選填）",
        trip_options,
        index=None if form["trip"] is None else trip_options.index(form["trip"]),
        horizontal=True,
        key=fkey("trip"),
    )
    cols = st.columns(2)
    with cols[0]:
        st.date_input("日期", value=form["date"], key=fkey("date"))
        st.time_input("最早可出發時間", value=form["earliest"], key=fkey("earliest"), step=dt.timedelta(minutes=15))
    with cols[1]:
        trip = read_inputs()["trip"]
        st.time_input(deadline_label(trip), value=form["deadline"], key=fkey("deadline"), step=dt.timedelta(minutes=15))
        if trip is None:
            st.caption(f"來回行程是「{T.DEADLINE_ROUND}」，單向行程是「{T.DEADLINE_ONE_WAY}」。")
        if current_scenario().get("anchor_start"):
            st.caption(T.ANCHOR_CAPTION)
        st.number_input(
            "出發油量（%，必填）", min_value=0, max_value=100, value=form["fuel"], step=1, key=fkey("fuel")
        )
        if "fuel" in errors:
            st.error(errors["fuel"])
    st.text_input("目標路線 GPX 的檔案路徑（選填）", value=form["gpx"], key=fkey("gpx"))
    st.caption("Skeleton 不讀取這個路徑的檔案（模擬）。")
    st.toggle("Snapshot Mode", value=form["snapshot"], key=fkey("snapshot"))
    st.button("規劃", type="primary", key="plan", on_click=on_plan)


def render_plan_steps() -> None:
    steps = ss.get("plan_steps")
    if not steps:
        return
    if steps == "complete":
        with st.status(f"規劃完成（模擬）：{len(S.PLAN_STEPS)} 個步驟都已完成", state="complete", expanded=False):
            for step in S.PLAN_STEPS:
                st.write(f"{step}：完成")
    elif steps == "clarify":
        with st.status("規劃暫停（模擬）：需要你補充", state="complete", expanded=False):
            st.write(f"{S.PLAN_STEPS[0]}：需要補充")
    elif steps == "route_error":
        with st.status("規劃停止（模擬）：沒有可採用的路線", state="error", expanded=False):
            st.write(f"{S.PLAN_STEPS[0]}：完成")
            st.write(f"{S.PLAN_STEPS[1]}：失敗")
    elif steps == "evaluation_failed":
        with st.status("規劃停止（模擬）：候選的評估沒有完成", state="error", expanded=False):
            for step in S.PLAN_STEPS[:3]:
                st.write(f"{step}：完成")
            st.write(f"{S.PLAN_STEPS[3]}：失敗")


def render_clarify(outcome: dict) -> None:
    questions = outcome["questions"]
    with st.chat_message("assistant", avatar=":material/help:"):
        st.markdown("**需要你補充**")
        st.write(T.CLARIFY_INTRO)
        for question in questions:
            st.radio(question["text"], question["options"], index=None, key=f"clarify_{question['id']}")
        if ss.get("clarify_error"):
            st.error(T.CLARIFY_INCOMPLETE)
        st.button(T.CLARIFY_BUTTON, key="clarify_reply", on_click=on_clarify_reply)


def render_clarify_answers(questions: list[dict]) -> None:
    answers = ss.get("clarify_answers") or {}
    rows = []
    for question in questions:
        answer = answers.get(question["id"])
        if (
            question["kind"] == "direction_if_round"
            and answers.get("trip") == T.TRIP_ONE_WAY
            and answer != T.OPTION_NO_REST
        ):
            # 單向時只忽略「去程」「回程」；「不安排這段休息」仍然取消那一筆休息（Issue #12 §2）。
            answer = T.DIRECTION_NOT_USED
        rows.append({"追問": question["text"], "回覆": answer})
    with st.chat_message("assistant", avatar=":material/help:"):
        st.write(T.CLARIFY_DONE)
        st.table(rows, hide_index=True)


def rests_after_clarify(plan: dict, questions: list[dict]) -> list[dict]:
    """Show the replied rest on the mock plan (display of the reply, not a scheduler)."""
    answers = ss.get("clarify_answers") or {}
    kinds = {q["kind"] for q in questions}
    replied = []
    if "rest_place" in kinds:
        place = answers.get("rest_place")
        if place != T.OPTION_NO_REST:
            direction = "—" if plan["trip_type"] == T.TRIP_ONE_WAY else "未決定（模擬；規格沒有定義這個組合）"
            replied.append({"地點": place, "方向": direction, "長度": "20 分鐘", "來源": "騎士指定（追問的回覆）"})
    if "direction" in kinds or "direction_if_round" in kinds:
        direction = answers.get("direction")
        if direction == T.OPTION_NO_REST:
            pass  # 「不安排這段休息」一律取消那一筆休息，單向與來回相同（Issue #12 §2）
        elif plan["trip_type"] == T.TRIP_ONE_WAY:
            # 單向時不使用「去程」「回程」的答案（或沒有回答），休息照行程描述排入、不分方向。
            replied.append({"地點": "示範觀景台", "方向": "—", "長度": "20 分鐘", "來源": "騎士指定（行程描述）"})
        else:
            replied.append({"地點": "示範觀景台", "方向": direction, "長度": "20 分鐘", "來源": "騎士指定（追問的回覆）"})
    if "break_duration" in kinds:
        replied.append({"地點": "示範老街", "方向": "去程", "長度": answers.get("duration"), "來源": "騎士指定（追問的回覆）"})
    defaults = [r for r in plan["rests"] if r["來源"].startswith("依 Profile")]
    return replied + defaults


def render_route_block(plan: dict) -> None:
    route = plan["route"]
    snapshot = bool((ss.get("plan_inputs") or {}).get("snapshot"))
    with st.container(border=True):
        with st.container(horizontal=True):
            st.markdown("**路線確認**")
            mock_badge()
            if route["source"] == "engine":
                st.badge("路線引擎", color="gray", icon=":material/route:")
                if snapshot:
                    st.badge("資料快照", color="blue", icon=":material/inventory_2:")
            else:
                st.badge("目標 GPX", color="gray", icon=":material/upload_file:")
        cols = st.columns(2)
        cols[0].metric("行程型態", plan["trip_type"])
        cols[1].metric("里程", f"{route['km']} 公里")
        if route["legs_km"]:
            st.write(f"去程 {route['legs_km'][0]} 公里；回程 {route['legs_km'][1]} 公里。")
        st.write(f"主要道路名稱（依行經順序）：{route['roads']}")
        st.caption(T.RIGHT_OF_WAY_ENGINE if route["source"] == "engine" else T.RIGHT_OF_WAY_GPX)
        if route["leg_diff_pct"]:
            st.info(T.fill(T.LEG_DIFF, 去回里程差的百分比=route["leg_diff_pct"]))


def render_stale() -> None:
    if ss.get("outcome") is None or not ss.get("plan_inputs"):
        return
    before, now = ss["plan_inputs"], read_inputs()
    changed = [FIELD_LABEL[name] for name in FORM_FIELDS if before.get(name) != now.get(name)]
    reasons = []
    if ss.get("stale_profile"):
        reasons.append("Profile 已更新。")
    if changed:
        reasons.append(f"上次規劃後變更了：{'、'.join(changed)}。")
    if reasons:
        st.warning(T.STALE_TEMPLATE.replace("{原因}", "".join(reasons)))


def render_route_error(code: str) -> None:
    message, todo = T.ROUTE_ERRORS[code]
    message = T.fill(message, 對不到的名稱=S.UNRESOLVED_NAME)
    st.error(f"{message}\n\n**可以怎麼做**\n\n- {todo}")


def render_unknown_rule(number: int, rule: dict) -> None:
    st.markdown(f"- **缺失的項目**：{rule['missing']}")
    st.markdown(f"- **原因**：{T.REASON_CLASS[rule['reason_class']]}（{rule['reason_class']}）。{rule['reason']}")
    st.markdown(f"- **來源與時間**：{rule['source']}")
    st.markdown(f"- **人工確認指引**：{T.GUIDANCE[(number, rule['reason_class'])]}")
    st.caption(T.SELF_CHECK_NOTE)


def render_rules(plan: dict) -> None:
    for number in (1, 2, 3, 4):
        rule = plan["rules"][number]
        with st.container(border=True):
            with st.container(horizontal=True):
                st.markdown(f"**{S.RULE_NAME[number]}**")
                badge(S.RULE_BADGE[rule["result"]])
            if rule["result"] == "UNKNOWN":
                render_unknown_rule(number, rule)
            else:
                st.markdown(f"- **原因**：{rule['detail']}")
                st.markdown(f"- **證據**：{'、'.join(rule['evidence'])}，見來源證據")


def weather_tables(plan: dict) -> None:
    weather = plan["weather"]
    if "one_way" in weather:
        st.table(weather["one_way"], hide_index=True)
    else:
        st.markdown("去程")
        st.table(weather["outbound"], hide_index=True)
        st.markdown("回程（規則 3 的範圍：折返點之後的全部回程）")
        st.table(weather["return"], hide_index=True)
    high = [row["區段"] for rows in weather.values() for row in rows if row["分類"] == T.HIGH_RAIN_LABEL]
    if high:
        with st.container(horizontal=True):
            st.badge(T.HIGH_RAIN_LABEL, color="yellow", icon=":material/warning:")
            st.write("、".join(high))
    st.caption(f"「{T.HIGH_RAIN_LABEL}」是降雨機率 70% 以上的路段。{T.HIGH_RAIN_CLASSIFICATION_NOTE}")
    if plan["outbound_high_rain"]:
        st.warning(T.OUTBOUND_HIGH_RAIN)
    st.caption(T.FORECAST_WINDOW_NOTE)


def coverage_sentence(plan: dict) -> None:
    kind, pct = plan["coverage"]
    if kind == "positive":
        st.info(T.fill(T.COVERAGE_POSITIVE, 涵蓋比例=pct))
    elif kind == "zero":
        st.info(T.COVERAGE_ZERO)
    else:
        st.info(T.COVERAGE_UNAVAILABLE)


def conditions_rows(plan: dict, rests: list[dict]) -> list[dict]:
    inputs = ss.get("plan_inputs") or {}
    deadline_name = T.DEADLINE_ROUND if plan["trip_type"] == T.TRIP_ROUND else T.DEADLINE_ONE_WAY
    rows = [
        {"項目": "行程型態", "內容": plan["trip_type"]},
        {"項目": "日期", "內容": str(inputs.get("date"))},
        {"項目": "最早可出發時間", "內容": str(inputs.get("earliest"))[:5]},
        {"項目": deadline_name, "內容": str(inputs.get("deadline"))[:5]},
        {"項目": "出發油量", "內容": f"{inputs.get('fuel')}%"},
        {"項目": "休息策略", "內容": plan["rest_policy"]},
    ]
    if rests:
        for rest in rests:
            direction = "" if rest["方向"] == "—" else f"（{rest['方向']}）"
            rows.append({"項目": "休息", "內容": f"{rest['地點']}{direction} {rest['長度']}；來源：{rest['來源']}"})
    else:
        rows.append({"項目": "休息", "內容": "沒有排入休息"})
    rows.append({"項目": "資料模式", "內容": "Snapshot Mode（固定的資料快照）" if inputs.get("snapshot") else "一般模式"})
    return rows


def render_trip_result(plan: dict, rests: list[dict]) -> None:
    with st.container(horizontal=True):
        badge(S.PLAN_BADGE[plan["status"]])
        mock_badge()
    st.caption("模擬：結果是這個情境寫定的資料，不依表單的內容計算。")
    if plan["status"] == "INFEASIBLE":
        st.error(f"**沒有可用的計畫。** {plan['infeasible_summary']}\n\n原因與代表性失敗候選在「Validation & Replanning」分頁。")
        st.subheader("路線摘要")
        st.write(f"{plan['route']['km']} 公里；{plan['route']['roads']}")
        coverage_sentence(plan)
        st.subheader("採用的條件")
        st.table(conditions_rows(plan, rests), hide_index=True)
        st.subheader("來源證據")
        st.table(plan["sources"], hide_index=True)
        return
    if plan["status"] == "CONDITIONAL":
        unknown = [(n, r) for n, r in plan["rules"].items() if r["result"] == "UNKNOWN"]
        items = "\n".join(
            f"{i}. **{S.RULE_NAME[n]}**：{T.GUIDANCE[(n, r['reason_class'])]}" for i, (n, r) in enumerate(unknown, 1)
        )
        st.warning(
            f"**出發前要確認的事項（{len(unknown)} 項）**\n\n{items}\n\n"
            "自行確認之後，計畫的狀態仍然是「有條件可行」；系統只依資料判定。"
        )
    metrics = plan["metrics"]
    cols = st.columns(2)
    cols[0].metric("最晚的可行出發時間", metrics["departure"])
    cols[1].metric(f"典型估計{metrics['arrive_label']}", metrics["eta_typ"])
    cols = st.columns(2)
    cols[0].metric(f"保守估計{metrics['arrive_label']}", metrics["eta_safe"], help=None)
    cols[1].metric("時間餘裕", metrics["margin"])
    st.caption("保守估計是典型估計加上安全餘裕的估計。")
    st.caption(T.ARRIVAL_NOTE)
    if plan["default_margin"]:
        st.caption(T.DEFAULT_MARGIN_NOTE)
    st.subheader("路線摘要")
    st.write(f"{plan['route']['km']} 公里；{plan['route']['roads']}")
    coverage_sentence(plan)
    st.subheader("說明")
    st.write(plan["explanation"])
    st.caption("來源：固定模板（由結構化欄位組成）。")
    st.write(plan["planner_note"])
    st.caption("來源：Planner 產生的補充說明（模擬文字），通過規則 5。")
    st.subheader("採用的條件")
    st.table(conditions_rows(plan, rests), hide_index=True)
    st.subheader("休息")
    if rests:
        st.table(rests, hide_index=True)
    else:
        st.write("沒有排入休息。")
    st.subheader("加油安排")
    st.table(plan["fuel"], hide_index=True)
    st.caption("加油安排（模擬）。安全保留油量 15%，來自 Rider Profile。")
    st.subheader("天氣")
    weather_tables(plan)
    st.subheader("來源證據")
    st.table(plan["sources"], hide_index=True)
    st.caption("本 Skeleton 的每一列都是模擬資料。")


def render_validation(plan: dict) -> None:
    if plan["status"] == "INFEASIBLE":
        st.subheader("無可行解")
        st.error(f"**原因摘要**：{plan['infeasible_summary']}")
        st.table(plan["fail_counts"], hide_index=True)
        rep = plan["representative"]
        with st.container(border=True):
            st.markdown(f"**代表性失敗候選：{rep['departure']} 出發**")
            with st.container(horizontal=True):
                badge(S.PLAN_BADGE["INFEASIBLE"])
                st.markdown("**這不是有效的建議。**")
            st.caption(f"選法：{rep['basis']}")
        st.info(
            "**替代方案（未經驗證，不會自動執行）**\n\n"
            "- 出發前先加油，提高出發油量後重新規劃。\n"
            "- 把最早可出發時間提前，或放寬期限。\n"
            "- 改日期，或改用其他的行程描述。\n\n"
            "以上都需要你修改表單後再按「規劃」，系統沒有驗證它們是否可行。"
        )
        st.subheader(f"逐條規則結果：代表性失敗候選（{rep['departure']} 出發）")
    else:
        st.subheader(f"逐條規則結果：推薦的候選（{plan['metrics']['departure']} 出發）")
    render_rules(plan)
    st.subheader("最終輸出的驗證")
    if plan["rule5"] is None:
        st.write("沒有可用的計畫，所以沒有產生說明文字。規則 5 不適用。")
    else:
        with st.container(border=True):
            with st.container(horizontal=True):
                st.markdown(f"**{S.RULE_NAME[5]}**")
                badge(S.RULE_BADGE[plan["rule5"]["result"]])
            st.markdown(f"- **結果**：{plan['rule5']['detail']}")
    with st.expander(f"全部候選（共 {len(plan['candidates'])} 個，唯讀）"):
        st.dataframe(plan["candidates"], hide_index=True, on_select="ignore")
        st.caption("唯讀表格，沒有列的選取。")
    st.subheader("重新規劃紀錄")
    st.table(plan["replans"], hide_index=True)


def render_outcome() -> None:
    outcome = ss.get("outcome")
    if outcome is None:
        if not ss.get("field_errors"):
            st.info("尚未規劃。填好上方的條件後按「規劃」。")
        return
    kind = outcome["kind"]
    if kind == "profile_only":
        st.info("模擬：這個情境只示範 Profile 區，沒有規劃結果。請切換到其他情境。")
        return
    if kind == "clarify":
        render_clarify(outcome)
        return
    if kind == "route_error":
        render_stale()
        render_route_error(outcome["code"])
        return
    if kind == "evaluation_failed":
        render_stale()
        st.error(T.EVALUATION_FAILED)
        return
    plan = S.PLANS[outcome["plan"]]
    questions = outcome.get("after_clarify")
    if questions:
        render_clarify_answers(questions)
        rests = rests_after_clarify(plan, questions)
    else:
        rests = plan["rests"]
    render_route_block(plan)
    render_stale()
    tab_result, tab_validation = st.tabs(["Trip Result", "Validation & Replanning"])
    with tab_result:
        render_trip_result(plan, rests)
    with tab_validation:
        render_validation(plan)


def main() -> None:
    st.set_page_config(page_title="Moto Touring Copilot — UI-0 Skeleton（模擬）", layout="centered")
    init_state()
    render_header()
    render_controls()
    render_profile()
    render_planner()
    render_plan_steps()
    render_outcome()


main()
