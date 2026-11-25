import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="상품 비교 및 최선의 선택 가이드", layout="centered")

st.title("상품 비교 및 최선의 선택 가이드")
st.write("비교할 상품을 선택하고 가격과 편익을 입력하면 기회비용을 계산해 최선의 선택을 알려드립니다.")

# 1) 리스트 선언: 상품별 이름 및 가격, 편익 리스트 정의
product_list = [
    {"name": "장난감", "price": 15000, "benefit": 18000},
    {"name": "게임현질", "price": 11000, "benefit": 16000},
    {"name": "불닭", "price": 4500, "benefit": 12000}
]

# 2) 입력 받기 (1): item으로 상품 선택
st.subheader("1. 비교할 상품 선택 (item)")
all_names = [p["name"] for p in product_list]
selected_items_names = st.multiselect(
    "비교할 상품을 2개 이상 선택하세요:",
    options=all_names,
    default=all_names
)

# 2) 입력 받기 (2): charge로 가격 및 편익 입력
st.subheader("2. 상품별 가격 및 편익 입력 (charge)")
input_data = []

if len(selected_items_names) > 0:
    cols = st.columns(len(selected_items_names))
    for i, name in enumerate(selected_items_names):
        # 기본값 찾기
        default_item = next(p for p in product_list if p["name"] == name)
        with cols[i]:
            st.markdown(f"**{name}**")
            charge_price = st.number_input(
                f"{name} 가격 (원)",
                min_value=0,
                value=default_item["price"],
                step=500,
                key=f"price_{name}"
            )
            charge_benefit = st.number_input(
                f"{name} 편익 (원)",
                min_value=0,
                value=default_item["benefit"],
                step=500,
                key=f"benefit_{name}"
            )
            input_data.append({
                "name": name,
                "price": charge_price,
                "benefit": charge_benefit,
                "surplus": charge_benefit - charge_price  # 순가치(편익 - 가격)
            })


# 3) 버튼 클릭 시 실행되는 check_risk() 함수 정의
def check_risk(items):
    if len(items) < 2:
        st.warning("⚠️ 비교할 상품을 2개 이상 선택(item)해 주세요.")
        return

    # 각 상품별 기회비용 계산 및 최소 기회비용 탐색
    min_opportunity_cost = float("inf")

    for i in range(len(items)):
        implicit_cost = 0  # 포기한 다른 대안 중 가장 큰 순가치(암묵적 비용)
        for j in range(len(items)):
            if i != j and items[j]["surplus"] > implicit_cost:
                implicit_cost = items[j]["surplus"]

        # 기회비용 = 명시적 비용(가격) + 암묵적 비용
        opp_cost = items[i]["price"] + implicit_cost
        items[i]["opportunity_cost"] = opp_cost

        if opp_cost < min_opportunity_cost:
            min_opportunity_cost = opp_cost

    # 4) 조건 판단 및 5) 반복 출력: for문을 이용해 상품별 리스트를 표 형태로 구성
    best_product_name = ""
    table_rows = []

    for item in items:
        opp_cost = item["opportunity_cost"]
        benefit = item["benefit"]

        # 조건 판단(if-elif-else): 기회비용이 다른 상품보다 크면 추천하지 않음
        if opp_cost > min_opportunity_cost:
            status_text = "추천하지 않음 (기회비용이 다른 상품보다 큼)"
        elif benefit < opp_cost:
            status_text = "추천하지 않음 (기회비용이 편익보다 큼)"
        else:
            status_text = "🏆 최선의 선택 (추천)"
            best_product_name = item["name"]

        # 표 생성용 데이터 리스트에 추가
        table_rows.append({
            "상품 이름 (item)": item["name"],
            "가격 (원)": f"{item['price']:,}원",
            "편익 (원)": f"{item['benefit']:,}원",
            "기회비용 (원)": f"{opp_cost:,}원",
            "조건 판단 결과": status_text
        })

    # 결과 텍스트 메시지 출력
    st.divider()
    if best_product_name != "":
        st.success(f"**{best_product_name}** 상품이 다른 제품과 비교해서 최선의 선택입니다.")
    else:
        st.error("모든 상품의 기회비용이 편익보다 크므로 추천하지 않습니다.")

    # 반복 출력: 구성된 리스트를 표 형태로 화면에 출력
    st.subheader("기회비용 결과값 목록 작성 표")
    st.table(table_rows)


# 3) 버튼 클릭 시 check_risk() 함수 실행
if st.button("기회비용 계산 및 최선의 선택 확인", type="primary", use_container_width=True):
    check_risk(input_data)
