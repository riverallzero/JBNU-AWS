# JBNU-AWS

## Current Data
| 날짜 | 시간 | 온도 | 습도 | 일사 | 풍속(1분평균) | 강우 |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-11-02 | 16:51:07 | 25.82 | 29.67 | 36.62 | 0.135 | 0 |

## Setting
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
