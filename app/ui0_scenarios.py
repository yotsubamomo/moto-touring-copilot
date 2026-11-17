"""Synthetic scenario data for the UI-0 mock-data skeleton (GitHub Issue #12).

Everything here is hand-written mock data. Road names, landmarks, times,
forecasts and checkpoints are fictional ("示範..."), not taken from any GPX,
ride, or ``data/`` file (UI0-9). There are no coordinates.

Every rule result, plan status, candidate label and Profile sufficiency flag is
a literal value in this module (CL-UI0-5). Nothing here computes a rule result,
a plan status or a ranking; the app only displays these values.

Standard library only (CL-UI0-1).
"""

from __future__ import annotations

import datetime as dt

import ui0_texts as T

MOCK_DATE = dt.date(2026, 12, 6)

# Public-landmark style gazetteer shown in "可用的公路與地標" (synthetic names).
GAZETTEER = [
    {"名稱": "示範公路甲線", "類型": "公路"},
    {"名稱": "示範公路乙線", "類型": "公路"},
    {"名稱": "示範縣道丙", "類型": "公路"},
    {"名稱": "示範車站", "類型": "出發錨點（代替住家的公開地標）"},
    {"名稱": "示範公園", "類型": "出發錨點（代替住家的公開地標）"},
    {"名稱": "示範觀景台", "類型": "地標"},
    {"名稱": "示範老街", "類型": "地標"},
    {"名稱": "示範山口", "類型": "地標"},
]

PLAN_STEPS = [
    "理解需求並整理休息與補給安排",
    "取得路線",
    "取得預報、暮光終、加油站與路況資料",
    "逐一評估候選並判定規則",
    "驗證輸出的說明文字",
]

PLAN_BADGE = {
    "FEASIBLE": ("FEASIBLE 可行", "green", ":material/check_circle:"),
    "CONDITIONAL": ("CONDITIONAL 有條件可行", "yellow", ":material/warning:"),
    "INFEASIBLE": ("INFEASIBLE 不可行", "red", ":material/cancel:"),
}
RULE_BADGE = {
    "PASS": ("PASS 通過", "green", ":material/check:"),
    "FAIL": ("FAIL 未通過", "red", ":material/close:"),
    "UNKNOWN": ("UNKNOWN 無法判定", "gray", ":material/help:"),
}
RULE_NAME = {
    1: "規則 1 日照與期限",
    2: "規則 2 油量",
    3: "規則 3 天氣",
    4: "規則 4 路況",
    5: "規則 5 可追溯",
}

# ---------------------------------------------------------------------------
# Profile states (coverage summary). "夠不夠" is a literal, not computed.
# ---------------------------------------------------------------------------

ENOUGH = "足夠"
NOT_ENOUGH = "不足（需要 30 段）"

PROFILES = {
    "empty": {
        "trips": 0,
        "segments": 0,
        "km": "0.0",
        "rows": [
            {"類別": T.CATEGORY_LOW, "路段數": 0, "來自幾趟": 0, "資料夠不夠": NOT_ENOUGH},
            {"類別": T.CATEGORY_MID, "路段數": 0, "來自幾趟": 0, "資料夠不夠": NOT_ENOUGH},
            {"類別": T.CATEGORY_HIGH, "路段數": 0, "來自幾趟": 0, "資料夠不夠": NOT_ENOUGH},
        ],
        "notes": [("warning", T.PROFILE_NO_GPX)],
    },
    "short": {
        "trips": 5,
        "segments": 92,
        "km": "286.4",
        "rows": [
            {"類別": T.CATEGORY_LOW, "路段數": 48, "來自幾趟": 5, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_MID, "路段數": 32, "來自幾趟": 4, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_HIGH, "路段數": 12, "來自幾趟": 3, "資料夠不夠": NOT_ENOUGH},
        ],
        "notes": [("warning", T.fill(T.PROFILE_CATEGORY_SHORT, 類別=T.CATEGORY_HIGH, N=12))],
    },
    "ok": {
        "trips": 9,
        "segments": 168,
        "km": "512.7",
        "rows": [
            {"類別": T.CATEGORY_LOW, "路段數": 70, "來自幾趟": 9, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_MID, "路段數": 58, "來自幾趟": 8, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_HIGH, "路段數": 40, "來自幾趟": 6, "資料夠不夠": ENOUGH},
        ],
        "notes": [("info", T.PROFILE_ALL_OK)],
    },
    "ok_more": {
        "trips": 12,
        "segments": 221,
        "km": "671.3",
        "rows": [
            {"類別": T.CATEGORY_LOW, "路段數": 92, "來自幾趟": 12, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_MID, "路段數": 76, "來自幾趟": 11, "資料夠不夠": ENOUGH},
            {"類別": T.CATEGORY_HIGH, "路段數": 53, "來自幾趟": 8, "資料夠不夠": ENOUGH},
        ],
        "notes": [("info", T.PROFILE_ALL_OK)],
    },
}

# Synthetic processing result shown after "更新 Profile". It does not depend on
# the selected files: they are never read (CL-UI0-2).
PROFILE_UPDATE_RESULT = {
    "added": 3,
    "duplicates": 1,
    "unreadable": [("1 個", "檔案中沒有軌跡點")],
}
PROFILE_UPDATE_STEPS = ["讀取選取的檔案", "略過內容重複的檔案", "切分路段並分類", "更新涵蓋度摘要"]

# ---------------------------------------------------------------------------
# Plans (results). All values are literals.
# ---------------------------------------------------------------------------

SOURCES_COMMON = [
    {"代號": "EV-ROUTE", "資料來源": "路線", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "全程"},
    {"代號": "EV-ETA", "資料來源": "個人配速表與 ETA", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "全程"},
    {"代號": "EV-SUN", "資料來源": "日照（民用暮光終）", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "終點"},
    {"代號": "EV-WX", "資料來源": "鄉鎮天氣預報", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "沿線鄉鎮"},
    {"代號": "EV-FUEL", "資料來源": "加油站與營業時間", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "示範加油站"},
    {"代號": "EV-ROAD", "資料來源": "路況事件", "來源類型": "模擬", "時間": "模擬，沒有取得時間", "涵蓋範圍": "全程"},
]
SOURCES_NO_ROAD = [row for row in SOURCES_COMMON if row["代號"] != "EV-ROAD"]


def _pass(detail: str, evidence: list[str]) -> dict:
    return {"result": "PASS", "detail": detail, "evidence": evidence}


def _fail(detail: str, evidence: list[str]) -> dict:
    return {"result": "FAIL", "detail": detail, "evidence": evidence}


def _unknown(missing: str, reason_class: str, reason: str, source: str) -> dict:
    return {
        "result": "UNKNOWN",
        "missing": missing,
        "reason_class": reason_class,
        "reason": reason,
        "source": source,
    }


RULE5_PASS = {"result": "PASS", "detail": "Planner 的說明第 1 次就通過。"}

PLAN_ROUND = {
    "id": "round",
    "trip_type": T.TRIP_ROUND,
    "status": "FEASIBLE",
    "route": {
        "source": "engine",
        "km": "96.4",
        "legs_km": ("47.0", "49.4"),
        "leg_diff_pct": "5.1",
        "roads": "去程：示範公路甲線 → 示範縣道丙；回程：示範縣道丙 → 示範公路乙線",
    },
    "coverage": ("positive", "38"),
    "metrics": {
        "departure": "09:15",
        "eta_typ": "15:40",
        "eta_safe": "16:35",
        "margin": "85 分",
        "arrive_label": "回到出發點",
    },
    "deadline": "18:00",
    "default_margin": False,
    "rest_policy": T.REST_POLICY_DEFAULT,
    "rests": [
        {"地點": "示範觀景台", "方向": "去程", "長度": "20 分鐘", "來源": "騎士指定（行程描述）"},
        {"地點": "示範山口（折返點）", "方向": "—", "長度": "15 分鐘", "來源": "依 Profile 排入的預設休息"},
    ],
    "fuel": [
        {"檢查點": "起點（示範車站）", "去程／回程": "—", "抵達時段": "—", "抵達時剩餘油量": "90%", "補油安排": "—", "站點營業狀態": "—"},
        {"檢查點": "示範加油站", "去程／回程": "去程", "抵達時段": "10:20–10:35", "抵達時剩餘油量": "68%", "補油安排": "不加油", "站點營業狀態": "不適用"},
        {"檢查點": "示範加油站", "去程／回程": "回程", "抵達時段": "14:05–14:40", "抵達時剩餘油量": "31%", "補油安排": "加滿", "站點營業狀態": "營業中（模擬）"},
        {"檢查點": "回到出發點", "去程／回程": "—", "抵達時段": "15:40–16:35", "抵達時剩餘油量": "82%", "補油安排": "—", "站點營業狀態": "—"},
    ],
    "weather": {
        "outbound": [
            {"區段": "去程前段", "採用的預報時段": "09:00–12:00", "時段長度": "3 小時", "降雨機率": "20%", "分類": "低降雨機率"},
            {"區段": "去程後段", "採用的預報時段": "09:00–12:00", "時段長度": "3 小時", "降雨機率": "75%", "分類": T.HIGH_RAIN_LABEL},
        ],
        "return": [
            {"區段": "回程前段", "採用的預報時段": "12:00–15:00", "時段長度": "3 小時", "降雨機率": "30%", "分類": "低降雨機率"},
            {"區段": "回程後段", "採用的預報時段": "15:00–18:00", "時段長度": "3 小時", "降雨機率": "40%", "分類": "中降雨機率"},
        ],
    },
    "outbound_high_rain": True,
    "rules": {
        1: _pass("保守估計 16:35 回到出發點，在最晚回到出發點時間 18:00 與民用暮光終 17:20 之前。", ["EV-ETA", "EV-SUN"]),
        2: _pass("每個檢查點的剩餘油量都高於安全保留油量 15%；回程在示範加油站加滿，抵達時段在營業時間內。", ["EV-FUEL"]),
        3: _pass("回程（規則 3 的範圍）沒有高降雨機率提醒的路段。", ["EV-WX"]),
        4: _pass("事件來源中沒有這條路線的封閉或管制事件。", ["EV-ROAD"]),
    },
    "rule5": RULE5_PASS,
    "explanation": "建議 09:15 出發。典型估計 15:40 回到出發點，保守估計 16:35，距離期限還有 85 分鐘。回程在示範加油站加滿。",
    "planner_note": "去程後段有高降雨機率提醒，出發前可以準備雨具。",
    "candidates": [
        {"出發時間": "08:30", "典型抵達": "14:55", "保守抵達": "15:50", "時間餘裕": "130 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "08:45", "典型抵達": "15:10", "保守抵達": "16:05", "時間餘裕": "115 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "09:00", "典型抵達": "15:25", "保守抵達": "16:20", "時間餘裕": "100 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "09:15", "典型抵達": "15:40", "保守抵達": "16:35", "時間餘裕": "85 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": "推薦"},
        {"出發時間": "09:30", "典型抵達": "15:55", "保守抵達": "16:50", "時間餘裕": "70 分", "計畫狀態": "INFEASIBLE 不可行", "FAIL 或 UNKNOWN 的規則": "3（FAIL）", "標籤": ""},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "5", "最佳狀態": "FEASIBLE 可行"},
    ],
    "sources": SOURCES_COMMON,
}

PLAN_ONE_WAY = {
    "id": "one_way",
    "trip_type": T.TRIP_ONE_WAY,
    "status": "FEASIBLE",
    "route": {
        "source": "engine",
        "km": "52.3",
        "legs_km": None,
        "leg_diff_pct": None,
        "roads": "示範公路甲線 → 示範縣道丙",
    },
    "coverage": ("zero", None),
    "metrics": {
        "departure": "13:30",
        "eta_typ": "15:20",
        "eta_safe": "15:55",
        "margin": "65 分",
        "arrive_label": "抵達終點",
    },
    "deadline": "17:00",
    "default_margin": False,
    "rest_policy": T.REST_POLICY_DEFAULT,
    "rests": [
        {"地點": "示範觀景台", "方向": "—", "長度": "15 分鐘", "來源": "依 Profile 排入的預設休息"},
    ],
    "fuel": [
        {"檢查點": "起點（示範車站）", "去程／回程": "—", "抵達時段": "—", "抵達時剩餘油量": "80%", "補油安排": "—", "站點營業狀態": "—"},
        {"檢查點": "示範加油站", "去程／回程": "—", "抵達時段": "14:25–14:45", "抵達時剩餘油量": "58%", "補油安排": "不加油", "站點營業狀態": "不適用"},
        {"檢查點": "終點（示範老街）", "去程／回程": "—", "抵達時段": "15:20–15:55", "抵達時剩餘油量": "44%", "補油安排": "—", "站點營業狀態": "—"},
    ],
    "weather": {
        "one_way": [
            {"區段": "前段（0–40%）", "採用的預報時段": "12:00–15:00", "時段長度": "3 小時", "降雨機率": "20%", "分類": "低降雨機率"},
            {"區段": "中段（40–80%）", "採用的預報時段": "12:00–15:00", "時段長度": "3 小時", "降雨機率": "30%", "分類": "低降雨機率"},
            {"區段": "最後 20%（規則 3 的範圍）", "採用的預報時段": "15:00–18:00", "時段長度": "3 小時", "降雨機率": "40%", "分類": "中降雨機率"},
        ],
    },
    "outbound_high_rain": False,
    "rules": {
        1: _pass("保守估計 15:55 抵達終點，在最晚抵達終點時間 17:00 與民用暮光終 17:20 之前。", ["EV-ETA", "EV-SUN"]),
        2: _pass("每個檢查點的剩餘油量都高於安全保留油量 15%。", ["EV-FUEL"]),
        3: _pass("路線最後 20%（規則 3 的範圍）沒有高降雨機率提醒的路段。", ["EV-WX"]),
        4: _pass("事件來源中沒有這條路線的封閉或管制事件。", ["EV-ROAD"]),
    },
    "rule5": RULE5_PASS,
    "explanation": "建議 13:30 出發。典型估計 15:20 抵達終點，保守估計 15:55，距離期限還有 65 分鐘。出發油量足夠，不需要加油。",
    "planner_note": "途中在示範觀景台休息 15 分鐘。",
    "candidates": [
        {"出發時間": "13:00", "典型抵達": "14:50", "保守抵達": "15:25", "時間餘裕": "95 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "13:15", "典型抵達": "15:05", "保守抵達": "15:40", "時間餘裕": "80 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "13:30", "典型抵達": "15:20", "保守抵達": "15:55", "時間餘裕": "65 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": "推薦"},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "3", "最佳狀態": "FEASIBLE 可行"},
    ],
    "sources": SOURCES_COMMON,
}

PLAN_TARGET_GPX = {
    "id": "target_gpx",
    "trip_type": T.TRIP_ONE_WAY,
    "status": "CONDITIONAL",
    "route": {
        "source": "gpx",
        "km": "61.8",
        "legs_km": None,
        "leg_diff_pct": None,
        "roads": "示範縣道丙 → 示範公路乙線",
    },
    "coverage": ("unavailable", None),
    "metrics": {
        "departure": "10:00",
        "eta_typ": "12:10",
        "eta_safe": "12:50",
        "margin": "130 分",
        "arrive_label": "抵達終點",
    },
    "deadline": "15:00",
    "default_margin": False,
    "rest_policy": T.REST_POLICY_DEFAULT,
    "rests": [
        {"地點": "示範觀景台", "方向": "—", "長度": "15 分鐘", "來源": "依 Profile 排入的預設休息"},
    ],
    "fuel": [
        {"檢查點": "起點", "去程／回程": "—", "抵達時段": "—", "抵達時剩餘油量": "85%", "補油安排": "—", "站點營業狀態": "—"},
        {"檢查點": "終點", "去程／回程": "—", "抵達時段": "12:10–12:50", "抵達時剩餘油量": "47%", "補油安排": "—", "站點營業狀態": "—"},
    ],
    "weather": {
        "one_way": [
            {"區段": "前段（0–40%）", "採用的預報時段": "09:00–12:00", "時段長度": "3 小時", "降雨機率": "20%", "分類": "低降雨機率"},
            {"區段": "中段（40–80%）", "採用的預報時段": "09:00–12:00", "時段長度": "3 小時", "降雨機率": "30%", "分類": "低降雨機率"},
            {"區段": "最後 20%（規則 3 的範圍）", "採用的預報時段": "UNKNOWN", "時段長度": "—", "降雨機率": "UNKNOWN", "分類": "UNKNOWN 無法判定（路段對不到鄉鎮）"},
        ],
    },
    "outbound_high_rain": False,
    "rules": {
        1: _pass("保守估計 12:50 抵達終點，在最晚抵達終點時間 15:00 與民用暮光終 17:20 之前。", ["EV-ETA", "EV-SUN"]),
        2: _pass("每個檢查點的剩餘油量都高於安全保留油量 15%。", ["EV-FUEL"]),
        3: _unknown(
            "路線最後 20% 的降雨機率",
            "NO_SOURCE",
            "最後 20% 的路段對不到鄉鎮，沒有對應的預報。",
            "EV-WX（模擬，沒有取得時間）",
        ),
        4: _pass("事件來源中沒有這條路線的封閉或管制事件。", ["EV-ROAD"]),
    },
    "rule5": RULE5_PASS,
    "explanation": "建議 10:00 出發。典型估計 12:10 抵達終點，保守估計 12:50，距離期限還有 130 分鐘。出發油量足夠，不需要加油。",
    "planner_note": "路線取自目標路線 GPX。",
    "candidates": [
        {"出發時間": "09:45", "典型抵達": "11:55", "保守抵達": "12:35", "時間餘裕": "145 分", "計畫狀態": "CONDITIONAL 有條件可行", "FAIL 或 UNKNOWN 的規則": "3（UNKNOWN）", "標籤": ""},
        {"出發時間": "10:00", "典型抵達": "12:10", "保守抵達": "12:50", "時間餘裕": "130 分", "計畫狀態": "CONDITIONAL 有條件可行", "FAIL 或 UNKNOWN 的規則": "3（UNKNOWN）", "標籤": "推薦"},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "2", "最佳狀態": "CONDITIONAL 有條件可行"},
    ],
    "sources": SOURCES_COMMON,
}

PLAN_UNKNOWN = {
    "id": "unknown",
    "trip_type": T.TRIP_ONE_WAY,
    "status": "CONDITIONAL",
    "route": {
        "source": "engine",
        "km": "58.9",
        "legs_km": None,
        "leg_diff_pct": None,
        "roads": "示範公路乙線 → 示範縣道丙",
    },
    "coverage": ("positive", "21"),
    "metrics": {
        "departure": "13:45",
        "eta_typ": "UNKNOWN",
        "eta_safe": "UNKNOWN",
        "margin": "UNKNOWN",
        "arrive_label": "抵達終點",
    },
    "deadline": "17:00",
    "default_margin": False,
    "rest_policy": T.REST_POLICY_DEFAULT,
    "rests": [],
    "fuel": [
        {"檢查點": "起點（示範車站）", "去程／回程": "—", "抵達時段": "—", "抵達時剩餘油量": "75%", "補油安排": "—", "站點營業狀態": "—"},
        {"檢查點": "終點（示範山口）", "去程／回程": "—", "抵達時段": "UNKNOWN", "抵達時剩餘油量": "UNKNOWN", "補油安排": "—", "站點營業狀態": "—"},
    ],
    "weather": {
        "one_way": [
            {"區段": "前段（0–40%）", "採用的預報時段": "UNKNOWN", "時段長度": "—", "降雨機率": "UNKNOWN", "分類": "UNKNOWN 無法判定（抵達時間無法估計）"},
            {"區段": "中段（40–80%）", "採用的預報時段": "UNKNOWN", "時段長度": "—", "降雨機率": "UNKNOWN", "分類": "UNKNOWN 無法判定（抵達時間無法估計）"},
            {"區段": "最後 20%（規則 3 的範圍）", "採用的預報時段": "UNKNOWN", "時段長度": "—", "降雨機率": "UNKNOWN", "分類": "UNKNOWN 無法判定（抵達時間無法估計）"},
        ],
    },
    "outbound_high_rain": False,
    "rules": {
        1: _unknown("保守抵達時間", "UPSTREAM_UNKNOWN", f"{T.CATEGORY_HIGH}沒有個人配速，ETA 的狀態是 unknown。", "EV-ETA（模擬，沒有取得時間）"),
        2: _unknown("各檢查點的抵達時間與剩餘油量", "UPSTREAM_UNKNOWN", "ETA 的狀態是 unknown。", "EV-ETA（模擬，沒有取得時間）"),
        3: _unknown("抵達時段的降雨機率", "UPSTREAM_UNKNOWN", "ETA 的狀態是 unknown，無法決定採用的預報時段。", "EV-ETA（模擬，沒有取得時間）"),
        4: _unknown("沿線的封閉與管制事件", "NO_SOURCE", "沒有可用的路況事件來源。", "沒有可用的來源"),
    },
    "rule5": RULE5_PASS,
    "explanation": "建議 13:45 出發。系統無法估計抵達時間，四條規則都無法判定，出發前請先確認下列事項。",
    "planner_note": "這條路線含有高曲率（連續彎道）的路段。",
    "candidates": [
        {"出發時間": "13:30", "典型抵達": "UNKNOWN", "保守抵達": "UNKNOWN", "時間餘裕": "UNKNOWN", "計畫狀態": "CONDITIONAL 有條件可行", "FAIL 或 UNKNOWN 的規則": "1、2、3、4（UNKNOWN）", "標籤": ""},
        {"出發時間": "13:45", "典型抵達": "UNKNOWN", "保守抵達": "UNKNOWN", "時間餘裕": "UNKNOWN", "計畫狀態": "CONDITIONAL 有條件可行", "FAIL 或 UNKNOWN 的規則": "1、2、3、4（UNKNOWN）", "標籤": "推薦"},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "2", "最佳狀態": "CONDITIONAL 有條件可行"},
    ],
    "sources": SOURCES_NO_ROAD,
}

PLAN_DEFAULT_MARGIN = {
    "id": "default_margin",
    "trip_type": T.TRIP_ONE_WAY,
    "status": "FEASIBLE",
    "route": {
        "source": "engine",
        "km": "44.6",
        "legs_km": None,
        "leg_diff_pct": None,
        "roads": "示範縣道丙 → 示範公路甲線",
    },
    "coverage": ("positive", "64"),
    "metrics": {
        "departure": "14:00",
        "eta_typ": "15:30",
        "eta_safe": "16:05",
        "margin": "55 分",
        "arrive_label": "抵達終點",
    },
    "deadline": "17:00",
    "default_margin": True,
    "rest_policy": T.REST_POLICY_NONE,
    "rests": [
        {"地點": "示範老街", "方向": "—", "長度": "10 分鐘", "來源": "騎士指定（行程描述）"},
    ],
    "fuel": [
        {"檢查點": "起點（示範公園）", "去程／回程": "—", "抵達時段": "—", "抵達時剩餘油量": "70%", "補油安排": "—", "站點營業狀態": "—"},
        {"檢查點": "終點（示範山口）", "去程／回程": "—", "抵達時段": "15:30–16:05", "抵達時剩餘油量": "41%", "補油安排": "—", "站點營業狀態": "—"},
    ],
    "weather": {
        "one_way": [
            {"區段": "前段（0–40%）", "採用的預報時段": "12:00–15:00", "時段長度": "3 小時", "降雨機率": "10%", "分類": "低降雨機率"},
            {"區段": "中段（40–80%）", "採用的預報時段": "15:00–18:00", "時段長度": "3 小時", "降雨機率": "20%", "分類": "低降雨機率"},
            {"區段": "最後 20%（規則 3 的範圍）", "採用的預報時段": "15:00–18:00", "時段長度": "3 小時", "降雨機率": "20%", "分類": "低降雨機率"},
        ],
    },
    "outbound_high_rain": False,
    "rules": {
        1: _pass("保守估計 16:05 抵達終點，在最晚抵達終點時間 17:00 與民用暮光終 17:20 之前。", ["EV-ETA", "EV-SUN"]),
        2: _pass("每個檢查點的剩餘油量都高於安全保留油量 15%。", ["EV-FUEL"]),
        3: _pass("路線最後 20%（規則 3 的範圍）沒有高降雨機率提醒的路段。", ["EV-WX"]),
        4: _pass("事件來源中沒有這條路線的封閉或管制事件。", ["EV-ROAD"]),
    },
    "rule5": RULE5_PASS,
    "explanation": "建議 14:00 出發。典型估計 15:30 抵達終點，保守估計 16:05，距離期限還有 55 分鐘。出發油量足夠，不需要加油。",
    "planner_note": "依行程描述在示範老街休息 10 分鐘，不安排其他休息。",
    "candidates": [
        {"出發時間": "13:45", "典型抵達": "15:15", "保守抵達": "15:50", "時間餘裕": "70 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": ""},
        {"出發時間": "14:00", "典型抵達": "15:30", "保守抵達": "16:05", "時間餘裕": "55 分", "計畫狀態": "FEASIBLE 可行", "FAIL 或 UNKNOWN 的規則": "—", "標籤": "推薦"},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "2", "最佳狀態": "FEASIBLE 可行"},
    ],
    "sources": SOURCES_COMMON,
}

PLAN_INFEASIBLE = {
    "id": "infeasible",
    "trip_type": T.TRIP_ONE_WAY,
    "status": "INFEASIBLE",
    "route": {
        "source": "engine",
        "km": "88.2",
        "legs_km": None,
        "leg_diff_pct": None,
        "roads": "示範公路甲線 → 示範公路乙線",
    },
    "coverage": ("positive", "45"),
    "metrics": None,
    "deadline": "17:00",
    "default_margin": False,
    "rest_policy": T.REST_POLICY_DEFAULT,
    "rests": [
        {"地點": "示範觀景台", "方向": "—", "長度": "15 分鐘", "來源": "依 Profile 排入的預設休息"},
    ],
    "infeasible_summary": "評估的 2 個候選全部不可行。最多候選違反的是規則 1 日照與期限（2 個）。",
    "fail_counts": [
        {"規則": RULE_NAME[1], "FAIL 的候選數": "2"},
        {"規則": RULE_NAME[2], "FAIL 的候選數": "0"},
        {"規則": RULE_NAME[3], "FAIL 的候選數": "0"},
        {"規則": RULE_NAME[4], "FAIL 的候選數": "0"},
    ],
    "representative": {
        "departure": "15:15",
        "basis": "FAIL 的規則數最少；平手時取出發時間最晚的。",
    },
    "rules": {
        1: _fail("保守估計 17:25 抵達終點，晚於最晚抵達終點時間 17:00。", ["EV-ETA", "EV-SUN"]),
        2: _pass("每個檢查點的剩餘油量都高於安全保留油量 15%。", ["EV-FUEL"]),
        3: _pass("路線最後 20%（規則 3 的範圍）沒有高降雨機率提醒的路段。", ["EV-WX"]),
        4: _pass("事件來源中沒有這條路線的封閉或管制事件。", ["EV-ROAD"]),
    },
    "rule5": None,
    "candidates": [
        {"出發時間": "15:00", "典型抵達": "16:35", "保守抵達": "17:10", "時間餘裕": "-10 分", "計畫狀態": "INFEASIBLE 不可行", "FAIL 或 UNKNOWN 的規則": "1（FAIL）", "標籤": ""},
        {"出發時間": "15:15", "典型抵達": "16:50", "保守抵達": "17:25", "時間餘裕": "-25 分", "計畫狀態": "INFEASIBLE 不可行", "FAIL 或 UNKNOWN 的規則": "1（FAIL）", "標籤": "代表性失敗候選"},
    ],
    "replans": [
        {"輪次": "初次", "結構化的變更": "—", "評估的候選數": "2", "最佳狀態": "INFEASIBLE 不可行"},
        {"輪次": "重新規劃 1", "結構化的變更": "取消預設休息以外沒有可調整的項目", "評估的候選數": "2", "最佳狀態": "INFEASIBLE 不可行"},
    ],
    "sources": SOURCES_COMMON,
}

PLANS = {
    plan["id"]: plan
    for plan in (PLAN_ROUND, PLAN_ONE_WAY, PLAN_TARGET_GPX, PLAN_UNKNOWN, PLAN_DEFAULT_MARGIN, PLAN_INFEASIBLE)
}

# ---------------------------------------------------------------------------
# Clarification (one round). Question kinds and their option lists.
# ---------------------------------------------------------------------------

REST_TEXT_UNMAPPED = "中途找個地方休息 20 分鐘"
REST_TEXT_DIRECTION = "在示範觀景台休息 20 分鐘"
REST_TEXT_NO_DURATION = "到示範老街休息一下"
REST_TEXT_STILL_UNMAPPED = "在山上的咖啡店休息 30 分鐘"
UNRESOLVED_NAME = "示範無名山徑"

ANCHOR_OPTIONS = ["示範車站（出發錨點）", "示範公園（出發錨點）"]
WAYPOINT_OPTIONS = ["示範觀景台", "示範老街"]

CLARIFY_START_TRIP_REST = [
    {"id": "start", "kind": "start", "text": T.Q_START_POINT, "options": ANCHOR_OPTIONS},
    {"id": "trip", "kind": "trip_type", "text": T.Q_TRIP_TYPE, "options": [T.TRIP_ROUND, T.TRIP_ONE_WAY]},
    {
        "id": "rest_place",
        "kind": "rest_place",
        "text": T.fill(T.Q_REST_UNMAPPED, 休息需求的原文=REST_TEXT_UNMAPPED),
        # Trip type is not known yet, so "折返點" is not offered.
        "options": WAYPOINT_OPTIONS + [T.OPTION_NO_REST],
    },
]

CLARIFY_ROUND_DIRECTION = [
    {
        "id": "entry",
        "kind": "entry_side",
        "text": T.fill(T.Q_ENTRY_SIDE, 公路="示範公路甲線"),
        "options": ["示範車站端", "示範山口端"],
    },
    {
        "id": "duration",
        "kind": "break_duration",
        "text": T.fill(T.Q_BREAK_DURATION, 休息需求的原文=REST_TEXT_NO_DURATION),
        "options": ["10 分鐘", "20 分鐘", "30 分鐘"],
    },
    {
        "id": "direction",
        "kind": "direction",
        "text": T.fill(T.Q_REST_DIRECTION, 休息需求的原文=REST_TEXT_DIRECTION),
        "options": [T.OPTION_OUTBOUND, T.OPTION_RETURN, T.OPTION_NO_REST],
    },
]

CLARIFY_TRIP_AND_DIRECTION = [
    {"id": "trip", "kind": "trip_type", "text": T.Q_TRIP_TYPE, "options": [T.TRIP_ROUND, T.TRIP_ONE_WAY]},
    {
        "id": "direction",
        "kind": "direction_if_round",
        "text": T.fill(T.Q_REST_DIRECTION_TRIP_TYPE_UNKNOWN, 休息需求的原文=REST_TEXT_DIRECTION),
        "options": [T.OPTION_OUTBOUND, T.OPTION_RETURN, T.OPTION_NO_REST],
    },
]

# ---------------------------------------------------------------------------
# Scenario menu. "outcome" is what pressing 「規劃」 shows (after the form
# checks pass). Form values are prefilled when the scenario is selected.
# ---------------------------------------------------------------------------


def _form(desc="", trip=None, earliest=dt.time(8, 0), deadline=dt.time(18, 0), fuel=80, gpx="", snapshot=False):
    return {
        "desc": desc,
        "trip": trip,
        "date": MOCK_DATE,
        "earliest": earliest,
        "deadline": deadline,
        "fuel": fuel,
        "gpx": gpx,
        "snapshot": snapshot,
    }


DESC_ROUND = "從示範車站出發，走示範公路甲線到示範山口折返，來回。去程在示範觀景台休息 20 分鐘。"
DESC_ONE_WAY = "從示範車站出發，走示範公路甲線接示範縣道丙到示範老街。"

SCENARIOS = [
    {
        "id": "s01",
        "label": "1. Profile：還沒有任何歷史 GPX（模擬）",
        "note": "Profile 區沒有任何歷史 GPX。這個情境只示範 Profile 區，按「規劃」不會產生結果。",
        "profile": "empty",
        "profile_after": "short",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY, deadline=dt.time(17, 0)),
        "outcome": {"kind": "profile_only"},
    },
    {
        "id": "s02",
        "label": "2. Profile：某個類別的路段不夠（模擬）",
        "note": "高曲率（連續彎道）的路段不夠。這個情境只示範 Profile 區，按「規劃」不會產生結果。",
        "profile": "short",
        "profile_after": "ok",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY, deadline=dt.time(17, 0)),
        "outcome": {"kind": "profile_only"},
    },
    {
        "id": "s03",
        "label": "3. Profile：三個類別都夠；多檔更新 Profile，舊結果標示為過期（模擬）",
        "note": "畫面上已經有上次規劃的結果。展開 Profile 區，選取多個合成的 .gpx 檔後按「更新 Profile」：顯示處理結果，舊的結果標示為過期，不會自動規劃。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0)),
        "outcome": {"kind": "plan", "plan": "one_way"},
        "preplanned": True,
    },
    {
        "id": "s04a",
        "label": "4a. 行程描述含門牌或座標的寫法：輸入保護（模擬）",
        "note": "行程描述含門牌的寫法，按「規劃」後不送出，欄位下方顯示固定訊息。可以改成「國道 3 號」「台 9 線」之類的公路寫法再按一次。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc="從中正路 123 號出發，避開國道 3 號，走示範縣道丙到示範老街。", trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0)),
        "outcome": {"kind": "plan", "plan": "one_way"},
    },
    {
        "id": "s04b",
        "label": "4b. 行程描述含「國道 3 號」：不被擋下（模擬）",
        "note": "「國道 3 號」與「台 9 線」是公路的寫法，不被輸入保護擋下；按「規劃」後顯示單向行程的模擬結果。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc="從示範車站出發，不要走國道 3 號，改走台 9 線接示範縣道丙到示範老街。", trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0)),
        "outcome": {"kind": "plan", "plan": "one_way"},
    },
    {
        "id": "s05",
        "label": "5. 追問：缺起點與行程型態，加上一筆對應不到地點的休息（模擬）",
        "note": "按「規劃」後出現一輪追問，同一個區塊列出三題。回覆後依所選的行程型態顯示模擬結果；模擬的抵達時間不隨回覆改變。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=f"走示範公路甲線到示範山口，{REST_TEXT_UNMAPPED}。"),
        "outcome": {"kind": "clarify", "questions": CLARIFY_START_TRIP_REST},
    },
    {
        "id": "s06a",
        "label": "6a. 追問：來回行程、途經點的休息沒有方向（模擬）",
        "note": "行程型態已選來回。追問同一輪列出進入端、休息長度與休息方向。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=f"從示範車站出發走示範公路甲線，{REST_TEXT_DIRECTION}，{REST_TEXT_NO_DURATION}。", trip=T.TRIP_ROUND),
        "outcome": {"kind": "clarify", "questions": CLARIFY_ROUND_DIRECTION},
    },
    {
        "id": "s06b",
        "label": "6b. 追問：行程型態與休息方向在同一輪（模擬）",
        "note": "行程型態沒有選，行程描述也沒有寫。方向的那一題標明「選擇來回時才需要回答」；回覆單向時方向的答案不使用。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=f"從示範車站出發走示範公路甲線到示範山口，{REST_TEXT_DIRECTION}。"),
        "outcome": {"kind": "clarify", "questions": CLARIFY_TRIP_AND_DIRECTION},
    },
    {
        "id": "s07",
        "label": "7. 追問之後仍然對應不到：行程描述欄下方的訊息，沒有計畫（模擬）",
        "note": "模擬一輪追問已經回覆、這段休息仍然對應不到地點的狀態：按「規劃」後不產生計畫，行程描述欄下方顯示固定訊息，不再追問。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=f"從示範車站出發，走示範公路甲線到示範山口，{REST_TEXT_STILL_UNMAPPED}。", trip=T.TRIP_ONE_WAY),
        "outcome": {"kind": "rest_unmapped", "source_text": REST_TEXT_STILL_UNMAPPED},
    },
    {
        "id": "s08",
        "label": "8. 來回行程的可行計畫：路線確認、涵蓋比例、去回里程差、去程高降雨機率提醒、騎士指定的休息（模擬）",
        "note": "來回行程。期限的名稱是「最晚回到出發點時間」；起點是出發錨點。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ROUND, trip=T.TRIP_ROUND, fuel=90),
        "anchor_start": True,
        "outcome": {"kind": "plan", "plan": "round"},
    },
    {
        "id": "s09",
        "label": "9. 單向行程的可行計畫：期限的名稱切換、涵蓋比例等於 0（模擬）",
        "note": "單向行程。切換「行程型態」可以看到期限的名稱改變，已填的時間是否保留照實記錄在 worklog。出發油量沒有預先填入（必填）：不填就按「規劃」會顯示欄位錯誤。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0), fuel=None),
        "anchor_start": True,
        "outcome": {"kind": "plan", "plan": "one_way"},
    },
    {
        "id": "s10",
        "label": "10. 目標 GPX 的路線：另一則路權提醒、涵蓋比例無法算出（模擬）",
        "note": "目標路線 GPX 的檔案路徑是合成的範例，Skeleton 不讀取這個檔案。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(trip=T.TRIP_ONE_WAY, earliest=dt.time(9, 0), deadline=dt.time(15, 0), gpx="synthetic/target-route-demo.gpx"),
        "outcome": {"kind": "plan", "plan": "target_gpx"},
    },
    {
        "id": "s11a",
        "label": "11a. 路線錯誤：not_in_gazetteer（模擬）",
        "note": "行程描述中的地點不在支援的公路與地標清單內。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=f"從示範車站出發，走{UNRESOLVED_NAME}到示範山口。", trip=T.TRIP_ONE_WAY),
        "outcome": {"kind": "route_error", "code": "not_in_gazetteer"},
    },
    {
        "id": "s11b",
        "label": "11b. 路線錯誤：routing_unavailable（模擬）",
        "note": "路線服務沒有產生可採用的路線。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY),
        "outcome": {"kind": "route_error", "code": "routing_unavailable"},
    },
    {
        "id": "s11c",
        "label": "11c. 路線錯誤：highway_in_route（模擬）",
        "note": "路線服務回傳的路線沒有通過國道檢查。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY),
        "outcome": {"kind": "route_error", "code": "highway_in_route"},
    },
    {
        "id": "s11d",
        "label": "11d. 路線錯誤：snapshot_missing（模擬）",
        "note": "Snapshot Mode 開啟，這個行程沒有路線快照。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY, snapshot=True),
        "outcome": {"kind": "route_error", "code": "snapshot_missing"},
    },
    {
        "id": "s11e",
        "label": "11e. 路線錯誤：target_gpx_invalid（模擬）",
        "note": "目標路線 GPX 無法當成路線使用。路徑是合成的範例，Skeleton 不讀取。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(trip=T.TRIP_ONE_WAY, gpx="synthetic/target-invalid-demo.gpx"),
        "outcome": {"kind": "route_error", "code": "target_gpx_invalid"},
    },
    {
        "id": "s11f",
        "label": "11f. 路線錯誤：target_gpx_not_round_trip（終點沒有回到起點）（模擬）",
        "note": "行程型態選來回，目標路線 GPX 的終點沒有回到起點。路徑是合成的範例，Skeleton 不讀取。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(trip=T.TRIP_ROUND, gpx="synthetic/target-one-way-demo.gpx"),
        "outcome": {"kind": "route_error", "code": "target_gpx_not_round_trip/end"},
    },
    {
        "id": "s11g",
        "label": "11g. 路線錯誤：target_gpx_not_round_trip（無法確認折返點）（模擬）",
        "note": "行程型態選來回，目標路線 GPX 回到起點，但無法確認折返點。路徑是合成的範例，Skeleton 不讀取。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(trip=T.TRIP_ROUND, gpx="synthetic/target-loop-demo.gpx"),
        "outcome": {"kind": "route_error", "code": "target_gpx_not_round_trip/turnaround"},
    },
    {
        "id": "s12",
        "label": "12. 評估失敗（模擬）",
        "note": "候選的評估沒有完成。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc=DESC_ONE_WAY, trip=T.TRIP_ONE_WAY),
        "outcome": {"kind": "evaluation_failed"},
    },
    {
        "id": "s13",
        "label": "13. 含 UNKNOWN 的計畫：沒有路況來源（規則 4）、抵達時間無法估計（模擬）",
        "note": "高曲率（連續彎道）的路段不夠，抵達時間無法估計；路況事件沒有來源。",
        "profile": "short",
        "profile_after": "ok",
        "form": _form(desc="從示範車站出發，走示範公路乙線接示範縣道丙到示範山口。", trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0)),
        "outcome": {"kind": "plan", "plan": "unknown"},
    },
    {
        "id": "s14",
        "label": "14. 預設的餘裕係數（行程不到 8 趟）；休息策略是「整趟不安排休息」（模擬）",
        "note": "保守估計使用預設的餘裕係數；行程描述明確要求整趟不安排休息，只保留另外指定的一段休息。Snapshot Mode 開啟。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc="從示範公園出發，走示範縣道丙接示範公路甲線到示範山口，整趟不要安排休息，只在示範老街停 10 分鐘。", trip=T.TRIP_ONE_WAY, earliest=dt.time(12, 0), deadline=dt.time(17, 0), fuel=70, snapshot=True),
        "anchor_start": True,
        "outcome": {"kind": "plan", "plan": "default_margin"},
    },
    {
        "id": "s15",
        "label": "15. 補充：無可行解（G3 沒有變更的呈現）（模擬）",
        "note": "全部候選都不可行，顯示一個代表性失敗候選。這不是 Issue 的 14 個情境之一，用來檢視 G3 沒有變更的呈現。",
        "profile": "ok",
        "profile_after": "ok_more",
        "form": _form(desc="從示範車站出發，走示範公路甲線接示範公路乙線到示範山口。", trip=T.TRIP_ONE_WAY, earliest=dt.time(15, 0), deadline=dt.time(17, 0)),
        "outcome": {"kind": "plan", "plan": "infeasible"},
    },
]

SCENARIO_BY_ID = {scenario["id"]: scenario for scenario in SCENARIOS}
