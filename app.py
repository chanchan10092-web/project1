<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>상품 비교 및 최선의 선택 가이드</title>
  <style>
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #f8fafc;
      color: #1e293b;
      margin: 0;
      padding: 24px;
    }
    .container { max-width: 860px; margin: 0 auto; }
    h1 { text-align: center; color: #0f172a; margin-bottom: 24px; }
    .box {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    h2 { font-size: 16px; color: #4f46e5; margin-top: 0; margin-bottom: 14px; }
    
    /* 1. 상품 선택 (item) */
    .item-group { display: flex; gap: 16px; flex-wrap: wrap; }
    .item-label {
      display: flex; align-items: center; gap: 6px;
      padding: 10px 16px; border: 1px solid #cbd5e1;
      border-radius: 8px; cursor: pointer; font-weight: 600;
      background: #f8fafc;
    }

    /* 2. 가격 및 편익 입력 (charge) */
    .charge-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }
    .charge-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 14px;
    }
    .charge-card strong { display: block; margin-bottom: 8px; font-size: 16px; }
    .charge-card label { display: block; font-size: 13px; color: #475569; margin-bottom: 6px; }
    .charge-card input {
      width: 100%; padding: 8px; margin-top: 4px;
      border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;
    }

    /* 3. 실행 버튼 */
    .run-btn {
      width: 100%;
      padding: 14px;
      background: #4f46e5;
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      margin-bottom: 20px;
    }
    .run-btn:hover { background: #4338ca; }

    /* 4. 결과 메시지 */
    .result-msg {
      background: #eef2ff;
      border: 2px solid #4f46e5;
      border-radius: 12px;
      padding: 18px;
      text-align: center;
      font-size: 18px;
      font-weight: 700;
      color: #1e1b4b;
      margin-bottom: 20px;
    }

    /* 5. 결과 테이블 */
    table { width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; }
    th, td { padding: 13px 10px; border-bottom: 1px solid #e2e8f0; }
    th { background: #f1f5f9; font-weight: 700; color: #334155; }
    .recommend-row { background-color: #eef2ff; font-weight: 700; }
    .not-recommend { color: #dc2626; font-weight: 600; }
    .recommend-text { color: #16a34a; font-weight: 700; }
  </style>
</head>
<body>

<div class="container">
  <h1>상품 비교 및 최선의 선택 가이드</h1>

  <!-- 입력 받기 (1): item으로 상품 선택 -->
  <div class="box">
    <h2>1. 비교할 상품 선택 (item)</h2>
    <div class="item-group" id="item-container"></div>
  </div>

  <!-- 입력 받기 (2): charge로 가격 및 편익 입력 -->
  <div class="box">
    <h2>2. 상품별 가격 및 편익 입력 (charge)</h2>
    <div class="charge-grid" id="charge-container"></div>
  </div>

  <!-- 3. 버튼 클릭 시 check_risk() 함수 실행 -->
  <button type="button" class="run-btn" onclick="check_risk()">
    기회비용 계산 및 결과 확인 (check_risk 실행)
  </button>

  <!-- 4. 조건 판단 결과 텍스트 메시지 -->
  <div class="result-msg" id="result-message">
    상품과 가격·편익을 확인한 뒤 위 버튼을 눌러주세요.
  </div>

  <!-- 5. 반복 출력: for문을 이용해 상품별 리스트를 표 형태로 화면에 출력 -->
  <div class="box">
    <h2>기회비용 결과값 목록 작성 표</h2>
    <table>
      <thead>
        <tr>
          <th>상품 이름 (item)</th>
          <th>가격 (원)</th>
          <th>편익 (원)</th>
          <th>기회비용 (원)</th>
          <th>조건 판단 결과</th>
        </tr>
      </thead>
      <tbody id="result-table-body"></tbody>
    </table>
  </div>
</div>

<script>
  // 1) 리스트 선언: 상품별 이름 및 가격, 편익 리스트 정의
  const productList = [
    { name: "장난감", price: 15000, benefit: 18000 },
    { name: "게임현질", price: 11000, benefit: 16000 },
    { name: "불닭", price: 4500, benefit: 12000 }
  ];

  // 초기 화면의 item(체크박스) 및 charge(가격·편익 입력칸) 생성
  function initUI() {
    const itemContainer = document.getElementById("item-container");
    const chargeContainer = document.getElementById("charge-container");

    for (let i = 0; i < productList.length; i++) {
      const product = productList[i];

      // item 선택 체크박스 생성
      itemContainer.innerHTML += `
        <label class="item-label">
          <input type="checkbox" name="item" value="${i}" checked>
          ${product.name}
        </label>
      `;

      // charge 가격 및 편익 입력폼 생성
      chargeContainer.innerHTML += `
        <div class="charge-card">
          <strong>${product.name}</strong>
          <label>
            가격 (charge - 명시적 비용):
            <input type="number" class="charge-price" data-index="${i}" value="${product.price}" step="500">
          </label>
          <label>
            편익 (charge - 예상 만족도):
            <input type="number" class="charge-benefit" data-index="${i}" value="${product.benefit}" step="500">
          </label>
        </div>
      `;
    }
  }

  // 3) 버튼 클릭 시 실행되는 check_risk() 함수
  function check_risk() {
    // 2) 입력 받기: 선택된 item과 입력된 charge(가격, 편익) 수집
    const itemCheckboxes = document.querySelectorAll('input[name="item"]:checked');
    const priceInputs = document.querySelectorAll('.charge-price');
    const benefitInputs = document.querySelectorAll('.charge-benefit');

    const selectedItems = [];
    for (let i = 0; i < itemCheckboxes.length; i++) {
      const idx = Number(itemCheckboxes[i].value);
      const priceVal = Number(priceInputs[idx].value) || 0;
      const benefitVal = Number(benefitInputs[idx].value) || 0;

      selectedItems.push({
        name: productList[idx].name,
        price: priceVal,
        benefit: benefitVal,
        surplus: benefitVal - priceVal // 순가치(편익 - 가격)
      });
    }

    const messageBox = document.getElementById("result-message");
    const tableBody = document.getElementById("result-table-body");

    if (selectedItems.length < 2) {
      messageBox.innerText = "비교할 상품을 2개 이상 선택(item)해 주세요.";
      tableBody.innerHTML = "";
      return;
    }

    // 각 상품별 기회비용 계산 및 최소 기회비용 찾기
    let minOpportunityCost = Infinity;

    for (let i = 0; i < selectedItems.length; i++) {
      let implicitCost = 0; // 포기한 다른 상품 중 가장 큰 순가치(암묵적 비용)

      for (let j = 0; j < selectedItems.length; j++) {
        if (i !== j && selectedItems[j].surplus > implicitCost) {
          implicitCost = selectedItems[j].surplus;
        }
      }

      // 기회비용 = 명시적 비용(가격) + 암묵적 비용
      selectedItems[i].opportunityCost = selectedItems[i].price + implicitCost;

      if (selectedItems[i].opportunityCost < minOpportunityCost) {
        minOpportunityCost = selectedItems[i].opportunityCost;
      }
    }

    // 4) 조건 판단 & 5) 반복 출력: for문을 이용해 상품별 리스트를 표 형태로 구성
    let bestProductName = "";
    let tableHTML = "";

    for (let i = 0; i < selectedItems.length; i++) {
      const current = selectedItems[i];
      let statusText = "";
      let rowClass = "";
      let statusClass = "";

      // 조건 판단: 기회비용이 다른 상품(최소 기회비용)보다 크면 추천하지 않음 문구 출력
      if (current.opportunityCost > minOpportunityCost) {
        statusText = "추천하지 않음 (기회비용이 다른 상품보다 큼)";
        statusClass = "not-recommend";
      } else if (current.benefit < current.opportunityCost) {
        statusText = "추천하지 않음 (기회비용이 편익보다 큼)";
        statusClass = "not-recommend";
      } else {
        statusText = "최선의 선택 (추천)";
        rowClass = "recommend-row";
        statusClass = "recommend-text";
        bestProductName = current.name;
      }

      // 표 행(tr) 생성
      tableHTML += `
        <tr class="${rowClass}">
          <td>${current.name}</td>
          <td>${current.price.toLocaleString()}원</td>
          <td>${current.benefit.toLocaleString()}원</td>
          <td><strong>${current.opportunityCost.toLocaleString()}원</strong></td>
          <td class="${statusClass}">${statusText}</td>
        </tr>
      `;
    }

    // 결과 문구 및 표 화면 출력
    if (bestProductName !== "") {
      messageBox.innerText = `${bestProductName} 상품이 다른 제품과 비교해서 최선의 선택입니다.`;
    } else {
      messageBox.innerText = "모든 상품의 기회비용이 편익보다 크므로 추천하지 않습니다.";
    }

    tableBody.innerHTML = tableHTML;
  }

  // 페이지 로드 시 입력 UI 생성 및 초기 계산 실행
  initUI();
  check_risk();
</script>

</body>
</html>
