document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('multiStepForm');
    const nextBtn = document.getElementById('nextBtn');
    const totalSteps = 3; // 현재 단계 수
    let currentStep = 1;

    // 유효성 검사 함수 정의
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

    // 입력 필드 변경 시 버튼 활성화/비활성화
    form.addEventListener('input', function () {
        if (validateStep(currentStep)) {
            nextBtn.disabled = false;
        } else {
            nextBtn.disabled = true;
        }
    });

    nextBtn.addEventListener('click', function () {
        if (!validateStep(currentStep)) {
            alert("필드를 비워둘 수 없습니다.");
            return;
        }

        if (currentStep < totalSteps) {
            // 현재 단계 숨기기
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('d-none');
            currentStep += 1;

            // 다음 단계 표시
            form.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('d-none');

            // 버튼 텍스트 변경
            if (currentStep === totalSteps) {
                nextBtn.textContent = "완료";
            } else {
                nextBtn.textContent = "다음";
            }

            // 버튼 비활성화 상태로 초기화
            nextBtn.disabled = true;
        } else {
            // 모든 단계를 완료했을 때, 폼을 제출
            form.submit();
        }
    });

    // 초기 버튼 상태 설정
    if (validateStep(currentStep)) {
        nextBtn.disabled = false;
    } else {
        nextBtn.disabled = true;
    }
});
