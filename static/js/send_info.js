function handleClick(button) {
    // 데이터 속성에서 제품 정보 가져오기
    const name = button.getAttribute("data-name");
    const mainFnctn = button.getAttribute("data-main-fnctn");
    const intakeHint = button.getAttribute("data-intake-hint");
    const baseStandard = button.getAttribute("data-base-standard");

    // 제품 상세 정보 업데이트
    document.getElementById("productTitle").textContent = name;
    document.getElementById("productFunction").textContent = mainFnctn || "정보 없음";
    document.getElementById("productIntake").textContent = intakeHint || "정보 없음";
    document.getElementById("productStandard").textContent = baseStandard || "정보 없음";

    // 제품 상세 정보 컨테이너 표시
    document.getElementById("productDetailsContainer").style.display = "block";
}

function closeProductDetails() {
    // 제품 상세 정보 컨테이너 숨기기
    document.getElementById("productDetailsContainer").style.display = "none";
}
