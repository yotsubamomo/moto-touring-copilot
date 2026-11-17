"""Fixed screen texts for the UI-0 mock-data skeleton (GitHub Issue #12).

Every constant in the "Issue #12 fixed texts" part is copied verbatim from the
Issue #12 body (UI0-3). Placeholders keep the Issue's own spelling, for example
``{休息需求的原文}`` or ``〈類別〉``; ``fill`` replaces them with synthetic values.

Texts that the Issue does not fix (question wording for start point, entry side,
trip type and rest duration; field errors; stale notice; mock labels) are in the
second part and are marked as skeleton wording for the UI Delta Review.

Standard library only (CL-UI0-1).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Issue #12 fixed texts (verbatim)
# ---------------------------------------------------------------------------

# 1. Profile
PROFILE_NO_GPX = (
    "還沒有歷史 GPX。沒有個人配速表時，系統無法估計抵達時間，和時間有關的規則會顯示 UNKNOWN。"
    "上傳一個檔案就可以開始。"
)
PROFILE_CATEGORY_SHORT = (
    "〈類別〉的路段還不夠（目前 N 段，需要 30 段）。路線含有這類路段時，系統無法估計抵達時間，"
    "會如實顯示 UNKNOWN。再上傳含有這類路段的行程就可以補上。"
)
PROFILE_ALL_OK = "三個類別的資料都足夠估計。新的 GPX 可以隨時再加入。"
PROFILE_PRIVACY = (
    "歷史 GPX 僅供本服務建立個人配速資料，不會傳送給外部語言模型或路線服務。畫面只顯示彙總資訊。"
)
CATEGORY_LOW = "低曲率（直路與緩彎）"
CATEGORY_MID = "中曲率（一般彎道）"
CATEGORY_HIGH = "高曲率（連續彎道）"
CATEGORIES = (CATEGORY_LOW, CATEGORY_MID, CATEGORY_HIGH)

# 2. Trip Planner: description, input guard, clarification
DESC_CAPTION = (
    "這段文字會送給語言模型。請用公路或地標描述，不要寫住家地址或座標。"
    "系統會擋下常見的門牌與座標寫法，但無法保證擋下所有私人位置。"
)
GUARD_MESSAGE = (
    "行程描述中有看起來像門牌地址或座標的內容，系統沒有送出這段文字。"
    "請改用公路或地標的名稱描述；起點在住家附近時，請用出發錨點。"
)
Q_REST_UNMAPPED = (
    "行程描述中的這段休息，系統沒有辦法對到這次行程的地點：「{休息需求的原文}」。"
    "請從下列選項選擇休息的地點，或選擇不安排這段休息。"
)
Q_REST_DIRECTION = (
    "行程描述中的這段休息，地點在去程與回程都會經過：「{休息需求的原文}」。"
    "請選擇要排在去程或回程，或選擇不安排這段休息。"
)
Q_REST_DIRECTION_TRIP_TYPE_UNKNOWN = (
    "（選擇來回時才需要回答）行程描述中的這段休息，如果是來回行程，地點在去程與回程都會經過："
    "「{休息需求的原文}」。請選擇要排在去程或回程，或選擇不安排這段休息。"
)
OPTION_TURNAROUND = "折返點"
OPTION_NO_REST = "不安排這段休息"
OPTION_OUTBOUND = "去程"
OPTION_RETURN = "回程"
REST_STILL_UNMAPPED = (
    "行程描述中的這段休息仍然沒有辦法排入：「{休息需求的原文}」。系統沒有產生計畫。"
    "請把休息的地點改成這次行程指定的途經點（來回行程也可以是折返點），或刪除這段休息後重新規劃。"
)

# 3. Trip type and deadline
TRIP_ROUND = "來回"
TRIP_ONE_WAY = "單向"
DEADLINE_ROUND = "最晚回到出發點時間"
DEADLINE_ONE_WAY = "最晚抵達終點時間"
DEADLINE_FIXED = "期限"
ANCHOR_CAPTION = "出發點不是住家；回到家的時間請自行加上。"

# 4. Route confirmation
RIGHT_OF_WAY_ENGINE = (
    "這條路線由路線引擎依開放圖資產生。系統用同一份開放圖資再檢查一次，沒有發現國道路段；"
    "這不是道路主管機關的驗證。其他道路的機車通行限制（例如部分快速公路與高架道路）系統無法保證，"
    "請出發前自行確認路權。"
)
RIGHT_OF_WAY_GPX = (
    "這條路線取自你提供的 GPX 或騎過的行程。系統沒有檢查國道與機車通行限制，請出發前自行確認路權。"
)
LEG_DIFF = (
    "去程與回程分別計算，里程相差約 {去回里程差的百分比}%。實際經過的道路可能不同，請核對道路名稱。"
)
COVERAGE_POSITIVE = (
    "配速資料中的路線涵蓋比例：這條路線約有 {涵蓋比例}% 的里程，幾何和你的配速資料接近（不分方向）。"
    "這個比例只比對用來建立個人配速表的行程；它不保證你實際走過同一條道路，也不代表你騎過的所有道路。"
    "抵達時間依你的個人配速表估計；配速資料沒有涵蓋的路段，估計的可信度較低。"
)
COVERAGE_ZERO = (
    "配速資料中的路線涵蓋比例：0%。配速資料中沒有幾何和這條路線接近的行程；"
    "這不表示你沒有騎過這條路，這個比例也不代表你騎過的所有道路。"
    "抵達時間依你在同類彎道上的個人配速估計，可信度較低。"
)
COVERAGE_UNAVAILABLE = "系統無法算出配速資料中的路線涵蓋比例。"

# 5. Route errors (six codes, seven texts) and evaluation failure:
#    code -> (message, what you can do)
ROUTE_ERRORS = {
    "not_in_gazetteer": (
        "行程描述中的「{對不到的名稱}」不在目前支援的公路與地標清單內，系統沒有產生路線。",
        "改用清單內的公路或地標重新描述；或提供目標路線 GPX。",
    ),
    "routing_unavailable": (
        "系統無法產生可採用的路線。",
        "請檢查起訖點與途經點，或改用已有的路線快照／目標 GPX。如果是路線服務暫時無法使用，請稍後再試。",
    ),
    "highway_in_route": (
        "路線服務回傳的路線沒有通過國道檢查，系統不採用這條路線。",
        "增加途經點讓路線避開國道；或提供目標路線 GPX。",
    ),
    "snapshot_missing": (
        "Snapshot Mode 只使用已保存的路線快照，這個行程沒有對應的快照。",
        "關閉 Snapshot Mode 後重新規劃；或改成有快照的行程。",
    ),
    "target_gpx_invalid": (
        "目標路線 GPX 無法當成路線使用：讀不到軌跡點、路線太短，或點與點之間的距離太遠。",
        "確認檔案路徑與內容；改用記錄較密的 GPX；或改用行程描述。",
    ),
    "target_gpx_not_round_trip/end": (
        "這個 GPX 不是來回的路線：終點沒有回到起點。",
        "請改選單向，或提供含回程的 GPX。",
    ),
    "target_gpx_not_round_trip/turnaround": (
        "系統無法確認這個 GPX 的折返點：軌跡不是明確的去回同路，而且沒有指定折返位置，"
        "或指定的位置不在軌跡的範圍內。",
        "指定折返位置（距起點的公里數，大於 0、小於軌跡總長）；或改選單向。",
    ),
}
EVALUATION_FAILED = (
    "候選的評估沒有完成，這次不提供建議的出發時間。請再按一次「規劃」；"
    "仍然失敗時，改用 Snapshot Mode 或稍後再試。"
)

# UNKNOWN presentation
SELF_CHECK_NOTE = "自行確認不會把這條規則改為 PASS。"
REASON_CLASS = {
    "NO_SOURCE": "沒有資料來源",
    "OUT_OF_COVERAGE": "超出涵蓋期間",
    "SOURCE_ERROR": "外部服務失敗",
    "MISSING_INPUT": "缺少必要輸入",
    "UPSTREAM_UNKNOWN": "上游結果為 UNKNOWN",
}
# (rule, reason class) -> fixed manual-check guidance
GUIDANCE = {
    (1, "SOURCE_ERROR"): "查詢當日的民用暮光終時間，確認保守抵達時間在天黑之前。",
    (1, "NO_SOURCE"): "查詢當日的民用暮光終時間，確認保守抵達時間在天黑之前。",
    (2, "NO_SOURCE"): "出發前確認這個加油站當天的營業時間，或先在起點加滿。",
    (2, "MISSING_INPUT"): "在 Rider Profile 補上油箱容量與平均油耗後重新規劃。",
    (3, "OUT_OF_COVERAGE"): "出發前查看氣象署的最新預報，確認抵達時段的降雨機率。",
    (3, "SOURCE_ERROR"): "出發前查看氣象署的最新預報，確認抵達時段的降雨機率。",
    (3, "NO_SOURCE"): "出發前查看氣象署的最新預報，確認抵達時段的降雨機率。",
    (4, "NO_SOURCE"): "出發前到公路主管機關的路況資訊，確認沿線有沒有封閉或管制。",
    (1, "UPSTREAM_UNKNOWN"): "系統無法估計抵達時間，這條規則無法判定。請自行估計騎乘時間後再決定是否出發。",
    (2, "UPSTREAM_UNKNOWN"): "系統無法估計抵達時間，這條規則無法判定。請自行估計騎乘時間後再決定是否出發。",
    (3, "UPSTREAM_UNKNOWN"): "系統無法估計抵達時間，這條規則無法判定。請自行估計騎乘時間後再決定是否出發。",
}

# 6. Weather, rests, arrival notes
HIGH_RAIN_LABEL = "高降雨機率提醒"
OUTBOUND_HIGH_RAIN = (
    "去程有路段是高降雨機率提醒。規則 3 在來回行程只檢查回程，所以規則 3 的 PASS 不代表去程不會下雨。"
)
FORECAST_WINDOW_NOTE = (
    "降雨機率是所列預報時段的數值，不是抵達那一刻的預報；各列採用的預報時段與時段長度見表中的欄位。"
)
ARRIVAL_NOTE = (
    "抵達時間已包含路上短暫停等（紅燈、車流）的估計，以及排入的休息與加油；不包含沒有安排的長時間停留。"
)
DEFAULT_MARGIN_NOTE = (
    "保守估計用的是預設的餘裕係數 0.20：可以用來估計餘裕的行程不到 8 趟，這個值不是由你的騎乘資料得出的。"
)
REST_POLICY_DEFAULT = "未特別限制，依 Profile 安排預設休息。"
REST_POLICY_NONE = "不套用預設休息；另外指定的休息仍會安排。"
HIGH_RAIN_CLASSIFICATION_NOTE = "它是本專題自訂的分類，不是氣象署的警特報，也不表示降雨強度。"

# ---------------------------------------------------------------------------
# Skeleton wording not fixed by Issue #12 (for the UI Delta Review)
# ---------------------------------------------------------------------------

Q_START_POINT = "行程描述中沒有起點。請選擇出發的地點。"
Q_ENTRY_SIDE = "行程描述中的「{公路}」有兩個進入端。請選擇從哪一端進入。"
Q_TRIP_TYPE = "行程描述中沒有說是來回或單向。請選擇行程型態。"
Q_BREAK_DURATION = "行程描述中的這段休息沒有寫多久：「{休息需求的原文}」。請選擇休息的長度。"
CLARIFY_INTRO = "規劃前還需要你補充下列項目（只有這一輪，全部選完後按一次「回覆並繼續規劃」）。"
CLARIFY_BUTTON = "回覆並繼續規劃"
CLARIFY_INCOMPLETE = "還有題目沒有回答。"
CLARIFY_DONE = "已回覆追問。追問只有一輪，不再追問。"
DIRECTION_NOT_USED = "未使用（行程型態是單向）"

FIELD_ERROR_NO_ROUTE_INPUT = "請填寫行程描述，或提供目標路線 GPX 的檔案路徑。"
FIELD_ERROR_FUEL = "出發油量是必填的（0–100%）。"
UPLOAD_NONE_SELECTED = "還沒有選取任何 .gpx 檔。"

STALE_TEMPLATE = "結果已過期。{原因}下方仍是上次規劃的結果；請按「規劃」重新計算。"


def fill(template: str, **values: object) -> str:
    """Replace the Issue-style placeholders in ``template``.

    ``values`` maps a placeholder name to its synthetic value. The supported
    placeholder spellings are ``{name}``, ``〈name〉`` and the ``目前 N 段`` count.
    A placeholder without a value is left in place so that a missing value is
    visible on screen instead of silently disappearing.
    """
    text = template
    for name, value in values.items():
        if name == "N":
            text = text.replace("目前 N 段", f"目前 {value} 段")
            continue
        text = text.replace("{" + name + "}", str(value))
        text = text.replace("〈" + name + "〉", str(value))
    return text
