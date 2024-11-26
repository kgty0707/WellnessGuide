document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('multiStepForm');
    const nextBtn = document.getElementById('nextBtn');
    const totalSteps = 3; // 총 단계 수
    let currentStep = 1;

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

    // 입력 단계별 유효성 검사
    function validateStep(step) {
        let isValid = true;
        if (step === 1) {
            const nameInput = form.querySelector('input[name="name"]');
            isValid = nameInput.value.trim() !== "";
        } else if (step === 2) {
            const heightInput = form.querySelector('input[name="height"]');
            const weightInput = form.querySelector('input[name="weight"]');
            isValid = heightInput.value.trim() !== "" && weightInput.value.trim() !== "";
        } else if (step === 3) {
            const phoneInput = form.querySelector('input[name="phone"]');
            isValid = phoneInput.value.trim() !== "";
        }
        return isValid;
    }

    // 폼 초기화
    function initializeForm() {
        currentStep = 1;

        // 모든 단계 숨기고 첫 번째 단계 표시
        document.querySelectorAll('.form-step').forEach((step, index) => {
            step.classList.toggle('d-none', index + 1 !== currentStep);
        });

        // 모든 입력 필드 초기화
        form.reset();

        // 버튼 텍스트와 상태 초기화
        nextBtn.textContent = "다음";
        nextBtn.disabled = !validateStep(currentStep);
    }

    // 입력 필드 변화에 따라 버튼 활성화/비활성화
    form.addEventListener('input', function () {
        nextBtn.disabled = !validateStep(currentStep);
    });

    nextBtn.addEventListener('click', function () {
        if (!validateStep(currentStep)) {
            alert("필드를 비워둘 수 없습니다.");
            return;
        }

        if (currentStep < totalSteps) {
            // 현재 단계 숨기기
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('d-none');
            currentStep++;

            // 다음 단계 표시
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('d-none');

            // 버튼 텍스트 업데이트
            nextBtn.textContent = currentStep === totalSteps ? "완료" : "다음";
            nextBtn.disabled = true;
        } else {
            showLoading(); // 로딩 화면 표시
            form.submit(); // 폼 제출
        }
    });

    // 뒤로 가기 시 폼 초기화
    window.addEventListener("pageshow", function () {
        hideLoading(); // 로딩 화면 초기화
        initializeForm(); // 폼 초기화
    });

    // 초기 상태 설정
    initializeForm();
});
