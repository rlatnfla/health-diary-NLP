# LLM이 '오늘 하루치의 일기'에서 추출해야 하는 일일 라이프스타일 메타데이터 정의
HEALTH_METADATA = {
    "burnout_count": {
        "type": int,
        "description": "오늘 일기 내용 중 심한 스트레스, 무기력증, 번아웃, 과도한 업무 피로감을 호소하거나 언급했다면 1, 없으면 0",
    },
    "sleep_lack_count": {
        "type": int,
        "description": "늦게 잤다, 밤을 새웠다, 수면 시간이 절대적으로 부족했다는 등 오늘 물리적인 수면 부족 상황이 언급되었다면 1, 없으면 0",
    },
    "insomnia_count": {
        "type": int,
        "description": "잠이 잘 안 왔다, 중간에 자꾸 깼다, 뒤척였다 등 오늘 수면의 질 저하나 불면 증상을 직접 호소했다면 1, 없으면 0",
    },
    "delivery_count": {
        "type": int,
        "description": "오늘 배달음식을 시켰다, 야식을 먹었다, 인스턴트(라면, 편의점 음식 등)나 자극적인 외식으로 대충 때웠다고 언급되었다면 1, 없으면 0",
    },
    "sedentary_count": {
        "type": int,
        "description": "오늘 하루 종일 누워만 있었다, 온종일 꼼짝 않고 앉아서 일만 했다 등 좌식 행동이나 신체 활동 결핍 상태가 감지된다면 1, 없으면 0",
    },
    "exercise_count": {
        "type": int,
        "description": "오늘 헬스, 러닝, 산책, 달리기, 수영 등 의도적으로 건강을 위해 운동이나 신체 활동을 수행했다고 직접 언급했다면 1, 없으면 0",
    },
    "breakfast_skip_count": {
        "type": int,
        "description": "오늘 아침 식사를 걸렀다, 늦잠 자서 아점을 먹었다 등 아침 식사 결식 행위가 명백히 감지된다면 1, 없으면 0",
    },
    "alcohol_count": {
        "type": int,
        "description": "오늘 술을 마셨다, 캔맥주 한 잔 했다, 회식 자리에서 과음했다 등 주류를 섭취한 행위가 언급되었다면 1, 없으면 0",
    },
    "msk_pain_count": {
        "type": int,
        "description": "오늘 목, 어깨, 허리, 뒷목, 손목 등 근골격계 부위의 뻐근함, 통증, 결림, 담 걸림 등을 직접 호소했다면 1, 없으면 0",
    },
    "vegetable_count": {
        "type": int,
        "description": "오늘 샐러드를 먹었다, 과일이나 야채를 챙겨 먹었다, 깨끗한 건강식을 의도해서 섭취했다고 언급되었다면 1, 없으면 0",
    },
    "regular_meal_count": {
        "type": int,
        "description": "오늘 제시간에 삼시세끼를 다 챙겨 먹었다, 거르지 않고 규칙적인 식사를 완수했다고 직접 언급되었다면 1, 없으면 0",
    },
}
