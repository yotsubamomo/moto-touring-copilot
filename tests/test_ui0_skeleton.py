"""Tests for the UI-0 Streamlit mock-data skeleton (GitHub Issue #12, SPEC-UI0).

Synthetic data only. The uploader tests use an empty file and a two-line
synthetic GPX header with no track points; no rider file is used (CL-UI0-2).
"""

from __future__ import annotations

import ast
import datetime as dt
import re
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_DIR = Path(__file__).resolve().parents[1] / "app"
APP_FILE = APP_DIR / "ui0_mock_app.py"
APP_SOURCES = sorted(APP_DIR.glob("*.py"))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import ui0_scenarios as S  # noqa: E402
import ui0_texts as T  # noqa: E402
from ui0_guard import guard_hits  # noqa: E402

SYNTHETIC_UPLOADS = [
    ("synthetic-empty.gpx", b"", "application/gpx+xml"),
    ("synthetic-header-only.gpx", b'<?xml version="1.0"?>\n<gpx version="1.1"></gpx>\n', "application/gpx+xml"),
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def run_app() -> AppTest:
    return AppTest.from_file(str(APP_FILE), default_timeout=60).run()


def select(at: AppTest, scenario_id: str) -> AppTest:
    return at.selectbox(key="scenario").set_value(scenario_id).run()


def plan(at: AppTest) -> AppTest:
    return at.button(key="plan").click().run()


def fk(at: AppTest, name: str) -> str:
    """Widget key of a form field for the current scenario (see ``fkey`` in the app)."""
    return f"f_{name}_{at.session_state['nonce']}"


def values(elements) -> list[str]:
    return [e.value for e in elements]


def all_text(at: AppTest) -> str:
    parts: list[str] = []
    for kind in ("markdown", "caption", "info", "warning", "error", "title", "header", "subheader"):
        parts.extend(str(e.value) for e in getattr(at, kind))
    for table in at.table:
        parts.append(str(table.value))
    return "\n".join(parts)


def parsed_sources() -> list[tuple[Path, ast.Module]]:
    return [(path, ast.parse(path.read_text(encoding="utf-8"))) for path in APP_SOURCES]


def string_constants() -> list[str]:
    found = []
    for _, tree in parsed_sources():
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                found.append(node.value)
    return found


# ---------------------------------------------------------------------------
# CL-UI0-1, CL-UI0-2: dependencies and upload handling (static)
# ---------------------------------------------------------------------------

LOCAL_MODULES = {"ui0_texts", "ui0_scenarios", "ui0_guard"}
FORBIDDEN_MODULES = {
    "moto_copilot", "os", "pathlib", "io", "tempfile", "shutil", "logging", "pickle", "sqlite3",
    "subprocess", "socket", "urllib", "http", "requests", "anthropic", "json",
}


def test_app_depends_only_on_streamlit_and_the_standard_library():
    for path, tree in parsed_sources():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                assert top not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
                assert top in LOCAL_MODULES or top == "streamlit" or top in sys.stdlib_module_names, (
                    f"{path.name} imports {name}"
                )


def test_app_never_reads_writes_or_logs_uploaded_content():
    banned_attrs = {"read", "readline", "readlines", "getvalue", "getbuffer", "seek", "write_bytes",
                    "write_text", "tofile", "dump"}
    for path, tree in parsed_sources():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    assert func.id not in {"open", "print", "exec", "eval"}, f"{path.name}: {func.id}()"
                if isinstance(func, ast.Attribute):
                    assert func.attr not in banned_attrs, f"{path.name}: .{func.attr}()"


def test_no_green_success_alert_is_used():
    for path, tree in parsed_sources():
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in {"success", "balloons", "chat_input"}:
                pytest.fail(f"{path.name} uses st.{node.attr}")


def test_app_never_creates_or_writes_a_rule_result_or_plan_status():
    """CL-UI0-5: rule results and plan statuses exist only as literals in ``ui0_scenarios``.

    The app and the other modules may read them (to pick a badge or a layout) but
    never assign a ``status``/``result`` value and never contain a status literal
    outside a comparison or a lookup table key.
    """
    status_words = {"FEASIBLE", "CONDITIONAL", "INFEASIBLE", "PASS", "FAIL", "UNKNOWN"}
    for path, tree in parsed_sources():
        if path.name in {"ui0_scenarios.py"}:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                        assert target.slice.value not in {"status", "result"}, f"{path.name}:{node.lineno}"
            if isinstance(node, ast.Dict):
                for key in node.keys:
                    assert not (isinstance(key, ast.Constant) and key.value in {"status", "result"}), (
                        f"{path.name}:{node.lineno} builds a status/result record"
                    )
            if isinstance(node, (ast.Return, ast.Assign)) and isinstance(node.value, ast.Constant):
                assert node.value.value not in status_words, f"{path.name}:{node.lineno} produces {node.value.value!r}"


# ---------------------------------------------------------------------------
# H-3: constrained wording; UI0-9: synthetic data only
# ---------------------------------------------------------------------------


def test_screen_text_has_no_forbidden_claims():
    for text in string_constants():
        assert "P90" not in text and "百分位" not in text and "分位數" not in text, text
        assert "這台電腦" not in text and "只留在" not in text and "本機" not in text, text
        assert "Google Maps" not in text, text
        if "警特報" in text:
            assert "不是氣象署的警特報" in text, text


def test_scenario_data_has_no_coordinates_and_only_synthetic_places():
    coordinate = re.compile(r"\d{1,3}\.\d{4,}")
    source = (APP_DIR / "ui0_scenarios.py").read_text(encoding="utf-8")
    assert not coordinate.search(source)
    for row in S.GAZETTEER:
        assert row["名稱"].startswith("示範")
    for scenario in S.SCENARIOS:
        assert "模擬" in scenario["label"]
        gpx = scenario["form"]["gpx"]
        assert gpx == "" or gpx.startswith("synthetic/")


def test_scenario_menu_covers_the_fourteen_issue_scenarios():
    ids = {s["id"] for s in S.SCENARIOS}
    for required in ["s01", "s02", "s03", "s04a", "s04b", "s05", "s06a", "s06b", "s07", "s08", "s09",
                     "s10", "s12", "s13", "s14"]:
        assert required in ids
    route_error_codes = {s["outcome"]["code"] for s in S.SCENARIOS if s["outcome"]["kind"] == "route_error"}
    assert route_error_codes == set(T.ROUTE_ERRORS)
    assert len(T.ROUTE_ERRORS) == 7


def test_plan_statuses_and_rule_results_are_literals_from_the_allowed_sets():
    for plan_data in S.PLANS.values():
        assert plan_data["status"] in {"FEASIBLE", "CONDITIONAL", "INFEASIBLE"}
        assert set(plan_data["rules"]) == {1, 2, 3, 4}
        for number, rule in plan_data["rules"].items():
            assert rule["result"] in {"PASS", "FAIL", "UNKNOWN"}
            if rule["result"] == "UNKNOWN":
                assert (number, rule["reason_class"]) in T.GUIDANCE


# ---------------------------------------------------------------------------
# Input guard (Issue #12 section 2 demo cases)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["中正路 123 號", "中正路一段 123 號", "123 號 5 樓", "0.1234, 0.5678", "從 0.123456，0.654321 出發"])
def test_guard_blocks_house_numbers_and_coordinate_pairs(text):
    assert guard_hits(text)


@pytest.mark.parametrize("text", ["國道 3 號", "台 9 線", "不要走國道 3 號，改走台 9 線", "示範公路甲線 30 公里", "休息 20 分鐘"])
def test_guard_does_not_block_road_names(text):
    assert not guard_hits(text)


def test_fill_replaces_issue_placeholders_and_keeps_missing_ones_visible():
    text = T.fill(T.PROFILE_CATEGORY_SHORT, 類別=T.CATEGORY_HIGH, N=12)
    assert text.startswith("高曲率（連續彎道）的路段還不夠（目前 12 段，需要 30 段）。")
    assert T.fill(T.LEG_DIFF) == T.LEG_DIFF
    assert "{去回里程差的百分比}" in T.fill(T.LEG_DIFF)


# ---------------------------------------------------------------------------
# AppTest: the screen
# ---------------------------------------------------------------------------


def test_every_scenario_renders_without_exception_and_is_labelled_simulated():
    at = run_app()
    for scenario in S.SCENARIOS:
        select(at, scenario["id"])
        plan(at)
        assert not at.exception, (scenario["id"], values(at.exception))
        text = all_text(at)
        assert "模擬資料：本頁不連接任何 API 或語言模型" in text
        assert T.PROFILE_PRIVACY in values(at.caption)
        assert not at.success


@pytest.mark.parametrize(
    ("scenario_id", "kind", "expected"),
    [
        ("s01", "warning", T.PROFILE_NO_GPX),
        ("s02", "warning", T.fill(T.PROFILE_CATEGORY_SHORT, 類別=T.CATEGORY_HIGH, N=12)),
        ("s03", "info", T.PROFILE_ALL_OK),
    ],
)
def test_profile_summary_texts(scenario_id, kind, expected):
    at = select(run_app(), scenario_id)
    assert expected in values(getattr(at, kind))
    assert len(at.metric) >= 3
    categories = [row for row in S.PROFILES[S.SCENARIO_BY_ID[scenario_id]["profile"]]["rows"]]
    assert [row["類別"] for row in categories] == list(T.CATEGORIES)


def test_update_profile_with_multiple_files_shows_result_and_marks_old_result_stale():
    at = select(run_app(), "s03")
    assert len(at.tabs) == 2  # the earlier result is on screen
    uploader = at.file_uploader[0]
    assert uploader.accept_multiple_files and uploader.allowed_type == [".gpx"]
    uploader.set_value(SYNTHETIC_UPLOADS).run()
    at.button(key="update_profile").click().run()
    assert not at.exception
    infos = values(at.info)
    assert any(v.startswith("處理結果（模擬，與選取的 2 個檔案的內容無關）：新增 3 個；略過 1 個內容重複的；") for v in infos)
    assert len(at.status) >= 1
    assert any("Profile 已更新" in v for v in values(at.warning))
    assert len(at.tabs) == 2  # updating the Profile does not trigger planning
    assert at.session_state["plan_steps"] == "complete"


def test_update_profile_without_files_does_not_process():
    at = select(run_app(), "s02")
    at.button(key="update_profile").click().run()
    assert T.UPLOAD_NONE_SELECTED in values(at.warning)
    assert not at.status


def test_input_guard_blocks_and_road_names_pass():
    at = plan(select(run_app(), "s04a"))
    assert T.GUARD_MESSAGE in values(at.error)
    assert not at.tabs
    at.text_area(key=fk(at, "desc")).set_value("從示範車站出發，不要走國道 3 號，改走台 9 線到示範老街。").run()
    plan(at)
    assert T.GUARD_MESSAGE not in values(at.error)
    assert len(at.tabs) == 2


def test_description_caption_is_fixed_text():
    at = run_app()
    assert T.DESC_CAPTION in values(at.caption)


def test_missing_description_and_gpx_and_fuel_are_field_errors():
    at = select(run_app(), "s09")
    assert at.number_input(key=fk(at, "fuel")).value is None  # scenario 9 starts with the fuel empty
    at.text_area(key=fk(at, "desc")).set_value("").run()
    plan(at)
    errors = values(at.error)
    assert T.FIELD_ERROR_NO_ROUTE_INPUT in errors
    assert T.FIELD_ERROR_FUEL in errors
    assert not at.tabs


def _clarify_radios(at: AppTest):
    return [r for r in at.radio if r.key and r.key.startswith("clarify_")]


def test_clarification_is_one_round_with_all_questions_together():
    at = plan(select(run_app(), "s05"))
    radios = _clarify_radios(at)
    assert len(radios) == 3
    rest = next(r for r in radios if r.key == "clarify_rest_place")
    assert rest.label == T.fill(T.Q_REST_UNMAPPED, 休息需求的原文=S.REST_TEXT_UNMAPPED)
    assert T.OPTION_TURNAROUND not in rest.options  # trip type is not known yet
    assert T.OPTION_NO_REST in rest.options
    assert not at.chat_input if hasattr(at, "chat_input") else True
    at.button(key="clarify_reply").click().run()
    assert T.CLARIFY_INCOMPLETE in values(at.error)
    at.radio(key="clarify_start").set_value(S.ANCHOR_OPTIONS[0])
    at.radio(key="clarify_trip").set_value(T.TRIP_ONE_WAY)
    at.radio(key="clarify_rest_place").set_value(T.OPTION_NO_REST).run()
    at.button(key="clarify_reply").click().run()
    assert not _clarify_radios(at)  # no second round
    assert T.CLARIFY_DONE in values(at.markdown)
    assert len(at.tabs) == 2


def test_direction_question_when_trip_type_is_also_asked():
    at = plan(select(run_app(), "s06b"))
    direction = at.radio(key="clarify_direction")
    assert direction.label == T.fill(T.Q_REST_DIRECTION_TRIP_TYPE_UNKNOWN, 休息需求的原文=S.REST_TEXT_DIRECTION)
    assert direction.options == [T.OPTION_OUTBOUND, T.OPTION_RETURN, T.OPTION_NO_REST]
    at.radio(key="clarify_trip").set_value(T.TRIP_ROUND).run()
    at.button(key="clarify_reply").click().run()
    assert T.CLARIFY_INCOMPLETE in values(at.error)  # round trip needs the direction
    at.radio(key="clarify_trip").set_value(T.TRIP_ONE_WAY).run()
    at.button(key="clarify_reply").click().run()
    assert not _clarify_radios(at)
    assert any(T.DIRECTION_NOT_USED in table.value.to_string() for table in at.table)


def test_direction_question_for_a_known_round_trip():
    at = plan(select(run_app(), "s06a"))
    keys = {r.key for r in _clarify_radios(at)}
    assert keys == {"clarify_entry", "clarify_duration", "clarify_direction"}
    assert at.radio(key="clarify_direction").label == T.fill(T.Q_REST_DIRECTION, 休息需求的原文=S.REST_TEXT_DIRECTION)


def test_rest_still_unmapped_shows_the_field_message_and_no_plan():
    at = plan(select(run_app(), "s07"))
    assert T.fill(T.REST_STILL_UNMAPPED, 休息需求的原文=S.REST_TEXT_STILL_UNMAPPED) in values(at.error)
    assert not at.tabs
    assert not _clarify_radios(at)


def test_round_trip_plan_shows_route_confirmation_and_fixed_sentences():
    at = plan(select(run_app(), "s08"))
    assert at.time_input(key=fk(at, "deadline")).label == T.DEADLINE_ROUND
    captions = values(at.caption)
    assert T.ANCHOR_CAPTION in captions
    assert T.RIGHT_OF_WAY_ENGINE in captions
    assert T.ARRIVAL_NOTE in captions
    assert T.FORECAST_WINDOW_NOTE in captions
    infos = values(at.info)
    assert T.fill(T.LEG_DIFF, 去回里程差的百分比="5.1") in infos
    assert T.fill(T.COVERAGE_POSITIVE, 涵蓋比例="38") in infos
    assert T.OUTBOUND_HIGH_RAIN in values(at.warning)
    text = all_text(at)
    assert "回程（規則 3 的範圍：折返點之後的全部回程）" in text
    assert "騎士指定（行程描述）" in text
    assert text.count("示範加油站") >= 2


def test_one_way_plan_deadline_label_switch_keeps_the_value():
    at = select(run_app(), "s09")
    assert at.time_input(key=fk(at, "deadline")).label == T.DEADLINE_ONE_WAY
    at.time_input(key=fk(at, "deadline")).set_value(dt.time(16, 45)).run()
    at.radio(key=fk(at, "trip")).set_value(T.TRIP_ROUND).run()
    assert at.time_input(key=fk(at, "deadline")).label == T.DEADLINE_ROUND
    assert at.time_input(key=fk(at, "deadline")).value == dt.time(16, 45)
    at.radio(key=fk(at, "trip")).set_value(T.TRIP_ONE_WAY).run()
    assert at.time_input(key=fk(at, "deadline")).label == T.DEADLINE_ONE_WAY
    assert at.time_input(key=fk(at, "deadline")).value == dt.time(16, 45)
    at.number_input(key=fk(at, "fuel")).set_value(80).run()
    plan(at)
    assert T.COVERAGE_ZERO in values(at.info)


def test_target_gpx_route_uses_the_other_right_of_way_sentence():
    at = plan(select(run_app(), "s10"))
    assert T.RIGHT_OF_WAY_GPX in values(at.caption)
    assert T.RIGHT_OF_WAY_ENGINE not in values(at.caption)
    assert T.COVERAGE_UNAVAILABLE in values(at.info)
    assert T.SELF_CHECK_NOTE in values(at.caption)


@pytest.mark.parametrize("scenario_id", [s["id"] for s in S.SCENARIOS if s["outcome"]["kind"] == "route_error"])
def test_route_errors_hide_status_departure_distance_and_roads(scenario_id):
    at = plan(select(run_app(), scenario_id))
    code = S.SCENARIO_BY_ID[scenario_id]["outcome"]["code"]
    message, todo = T.ROUTE_ERRORS[code]
    message = T.fill(message, 對不到的名稱=S.UNRESOLVED_NAME)
    assert values(at.error) == [f"{message}\n\n**可以怎麼做**\n\n- {todo}"]
    assert not at.tabs
    assert not at.metric[3:]  # only the three Profile metrics remain
    text = all_text(at)
    assert "路線確認" not in text and "主要道路名稱" not in text and "FEASIBLE" not in text


def test_evaluation_failure_shares_the_error_layout():
    at = plan(select(run_app(), "s12"))
    assert values(at.error) == [T.EVALUATION_FAILED]
    assert not at.tabs
    assert "最晚的可行出發時間" not in all_text(at)


def test_unknown_plan_shows_four_items_and_guidance():
    at = plan(select(run_app(), "s13"))
    text = all_text(at)
    assert "CONDITIONAL 有條件可行" in text
    assert T.GUIDANCE[(4, "NO_SOURCE")] in text
    assert T.GUIDANCE[(1, "UPSTREAM_UNKNOWN")] in text
    for item in ("缺失的項目", "原因", "來源與時間", "人工確認指引"):
        assert f"**{item}**" in text
    assert values(at.caption).count(T.SELF_CHECK_NOTE) == 4
    assert "UNKNOWN" in [m.value for m in at.metric]


def test_default_margin_and_no_rest_policy():
    at = plan(select(run_app(), "s14"))
    assert T.DEFAULT_MARGIN_NOTE in values(at.caption)
    assert T.REST_POLICY_NONE in all_text(at)


def test_field_change_marks_result_stale_without_replanning():
    at = plan(select(run_app(), "s08"))
    at.number_input(key=fk(at, "fuel")).set_value(55).run()
    assert any("出發油量" in v and v.startswith("結果已過期。") for v in values(at.warning))
    assert len(at.tabs) == 2


def test_candidate_table_is_read_only():
    at = plan(select(run_app(), "s08"))
    assert at.dataframe
    for frame in at.dataframe:
        assert not frame.proto.selection_mode


# ---------------------------------------------------------------------------
# R1-F1 regression: 「不安排這段休息」 cancels the rest also when the reply is 單向
# ---------------------------------------------------------------------------


def _rest_rows(at: AppTest) -> list[dict]:
    """Rows of the result's 「休息」 table (columns 地點／方向／長度／來源)."""
    for table in at.table:
        frame = table.value
        if list(frame.columns) == ["地點", "方向", "長度", "來源"]:
            return frame.to_dict("records")
    return []


def _answer_of(at: AppTest, question_text: str):
    for table in at.table:
        frame = table.value
        if list(frame.columns) == ["追問", "回覆"]:
            for row in frame.to_dict("records"):
                if row["追問"] == question_text:
                    return row["回覆"]
    raise AssertionError("answers table not found")


def _reply_6b(trip: str, direction: str | None) -> AppTest:
    at = plan(select(run_app(), "s06b"))
    at.radio(key="clarify_trip").set_value(trip)
    if direction is not None:
        at.radio(key="clarify_direction").set_value(direction)
    at.run()
    at.button(key="clarify_reply").click().run()
    assert not at.exception
    assert not _clarify_radios(at), "the reply was not accepted"
    return at


DIRECTION_TEXT = T.fill(T.Q_REST_DIRECTION_TRIP_TYPE_UNKNOWN, 休息需求的原文=S.REST_TEXT_DIRECTION)


def _rider_rests(at: AppTest) -> list[dict]:
    return [row for row in _rest_rows(at) if row["來源"].startswith("騎士指定")]


def test_one_way_reply_with_no_rest_cancels_the_rest():
    at = _reply_6b(T.TRIP_ONE_WAY, T.OPTION_NO_REST)
    assert _rider_rests(at) == []
    assert _answer_of(at, DIRECTION_TEXT) == T.OPTION_NO_REST
    # Only the Profile default rest of the mock one-way plan remains; it is not the cancelled request.
    assert [row["來源"] for row in _rest_rows(at)] == ["依 Profile 排入的預設休息"]


@pytest.mark.parametrize("direction", [T.OPTION_OUTBOUND, T.OPTION_RETURN, None])
def test_one_way_reply_ignores_only_the_outbound_or_return_choice(direction):
    at = _reply_6b(T.TRIP_ONE_WAY, direction)
    assert _rider_rests(at) == [{"地點": "示範觀景台", "方向": "—", "長度": "20 分鐘", "來源": "騎士指定（行程描述）"}]
    assert _answer_of(at, DIRECTION_TEXT) == T.DIRECTION_NOT_USED


def test_round_trip_reply_with_no_rest_cancels_the_rest():
    at = _reply_6b(T.TRIP_ROUND, T.OPTION_NO_REST)
    assert _rider_rests(at) == []
    assert _answer_of(at, DIRECTION_TEXT) == T.OPTION_NO_REST


@pytest.mark.parametrize("direction", [T.OPTION_OUTBOUND, T.OPTION_RETURN])
def test_round_trip_reply_uses_the_chosen_direction(direction):
    at = _reply_6b(T.TRIP_ROUND, direction)
    assert _rider_rests(at) == [{"地點": "示範觀景台", "方向": direction, "長度": "20 分鐘", "來源": "騎士指定（追問的回覆）"}]
    assert _answer_of(at, DIRECTION_TEXT) == direction


def test_known_round_trip_direction_no_rest_cancels_the_rest():
    at = plan(select(run_app(), "s06a"))
    at.radio(key="clarify_entry").set_value("示範車站端")
    at.radio(key="clarify_duration").set_value("10 分鐘")
    at.radio(key="clarify_direction").set_value(T.OPTION_NO_REST).run()
    at.button(key="clarify_reply").click().run()
    assert not _clarify_radios(at)
    assert "示範觀景台" not in [row["地點"] for row in _rider_rests(at)]
