# JBNU-AWS

## Current Data
| 날짜 | 시간 | 온도 | 습도 | 일사 | 풍속(1분평균) | 강우 |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-11-02 | 17:01:33 | 25.55 | 31.13 | 28.61 | 0.42 | 0 |

## Setting
### Cron
- 10분마다 AWS에서 기상 데이터를 수집후 ThingSpeak에 업로드
- ThingSpeak에 실시간으로 업로드 된 데이터를 위 **Current Data**에 테이블 형태로 입력

```
schedule:
- cron:  "*/10 * * * *"
```

### GitHub
⚙︎ Repository Settings - (Security) Secrets and variables - Actions - New repository secret으로 생성
- WRITE_KEY: thingspeak write api key 입력
- READ_KEY: thingspeak read api key 입력

### ThingSpeak

<details>
<summary>Channel 만들기</summary>

- field 생성
- github 링크 첨부

![](.asset/thingspeak-channel.png)
</details>

<details>
<summary>API 가져오기</summary>

![](.asset/thingspeak-api.png)
</details>
