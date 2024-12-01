document.addEventListener('DOMContentLoaded', function () {
    let totalSteps = 0;
    let form = null; // 현재 활성화된 폼을 저장할 변수
    let currentStep = 1; // 현재 단계 초기값
    let nextBtn = null; // 현재 활성화된 "다음" 버튼
    let stepIndicator = null; // 단계 번호를 표시할 요소

    // 폼 선택 버튼 이벤트
    document.getElementById('formOption1').addEventListener('click', () => {
        activateForm('form1', 'multiStepForm1', 'nextBtn1', 'in_number1', 3);
    });

    document.getElementById('formOption2').addEventListener('click', () => {
        activateForm('form2', 'multiStepForm2', 'nextBtn2', 'in_number2', 5);
    });

    // 폼 활성화
    function activateForm(formId, formElementId, nextBtnId, stepIndicatorId, steps) {
        // 초기 선택 화면 숨기기
        document.getElementById('initialChoice').classList.add('d-none');
        // 선택된 폼 표시
        document.getElementById(formId).classList.remove('d-none');

        // 폼 및 버튼, 단계 표시 요소 설정
        form = document.getElementById(formElementId);
        nextBtn = document.getElementById(nextBtnId);
        stepIndicator = document.getElementById(stepIndicatorId);
        totalSteps = steps;
        currentStep = 1;

        // 기존 클릭 이벤트 제거 후 새로 추가
        nextBtn.removeEventListener('click', handleNextClick); // 중복 방지
        nextBtn.addEventListener('click', handleNextClick);

        // 입력 필드 변화에 따른 버튼 활성화/비활성화
        form.addEventListener('input', function () {
            nextBtn.disabled = !validateStep(currentStep);
        });

        initializeForm();
    }

    // "다음" 버튼 클릭 이벤트 핸들러
    function handleNextClick() {
        if (!validateStep(currentStep)) {
            alert("필드를 비워둘 수 없습니다.");
            return;
        }

        if (currentStep < totalSteps) {
            // 현재 단계 숨기기
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('d-none');
            currentStep++;

            // 현재 단계 업데이트
            updateStepDisplay();

            // 다음 단계 표시
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('d-none');

            // 버튼 텍스트 업데이트
            nextBtn.textContent = currentStep === totalSteps ? "완료" : "다음";
            nextBtn.disabled = true;
        } else {
            showLoading();
            form.submit();
        }
    }

    // 입력 단계별 유효성 검사
    function validateStep(step) {
        if (!form) return false;

        let isValid = true;

        if (step === 1) {
            const nameInput = form.querySelector('input[name="name"]');
            const genderInput = form.querySelector('input[name="gender"]:checked');
            const ageSelect = form.querySelector('select[name="age"]');
            isValid =
                nameInput?.value.trim() !== "" &&
                genderInput !== null &&
                ageSelect?.value.trim() !== "";
        } else if (step === 2) {
            const heightInput = form.querySelector('input[name="height"]');
            const weightInput = form.querySelector('input[name="weight"]');
            isValid = heightInput?.value.trim() !== "" && weightInput?.value.trim() !== "";
        } else if (step === 3) {
            const systolicInput = form.querySelector('input[name="systolic"]');
            const diastolicInput = form.querySelector('input[name="diastolic"]');
            isValid =
                systolicInput?.value.trim() !== "" &&
                diastolicInput?.value.trim() !== "";
        }

        return isValid;
    }

    // 폼 초기화
    function initializeForm() {
        if (!form || !stepIndicator) return;

        currentStep = 1;

        // 모든 단계 숨기고 첫 번째 단계 표시
        form.querySelectorAll('.form-step').forEach((step, index) => {
            step.classList.toggle('d-none', index + 1 !== currentStep);
        });

        // 현재 단계 표시 업데이트
        updateStepDisplay();

        // 모든 입력 필드 초기화
        form.reset();

        // 버튼 텍스트와 상태 초기화
        nextBtn.textContent = "다음";
        nextBtn.disabled = !validateStep(currentStep);
    }

    // 현재 단계를 UI에 업데이트
    function updateStepDisplay() {
        if (stepIndicator) {
            stepIndicator.textContent = currentStep;
        }
    }

    // 로딩 화면의 순차적 텍스트 표시
    function showSequentialTexts() {
        const texts = document.querySelectorAll(".loading-text");
        let index = 0;

        function showNextText() {
            texts.forEach((text, i) => {
                text.style.display = i === index ? "block" : "none";
            });

            if (index < texts.length - 1) {
                index++;
                setTimeout(showNextText, 1500);
            }
        }

        showNextText();
    }

    // 로딩 화면 표시
    function showLoading() {
        document.getElementById("loadingOverlay").style.display = "flex";
        showSequentialTexts();
    }

    // 로딩 화면 숨김
    function hideLoading() {
        document.getElementById("loadingOverlay").style.display = "none";
        document.querySelectorAll(".loading-text").forEach(text => {
            text.style.display = "none";
        });
    }

    // 뒤로 가기 시 폼 초기화
    window.addEventListener("pageshow", function () {
        hideLoading();
        initializeForm();
    });
});
