# Nanjing University Auto Health-check Punch-in Tool (南大自动健康打卡工具)

## prerequisites

1. install docker
2. download image and start container `docker run -d -p 3000:3000 browserless/chrome `
3. install packages `pip install selenium schedule`
4. set env variables `export EHALL_USERNAME=xxx; export EHALL_PASSWARD=xxx; export DAKA_ADRESS=xxx`

## usage

start the script `python daka.py`

## remark

```python
@repeat(every().day.at('10:30'))  # (1)
# @repeat(every(2).seconds) # (2)
def job():
    msg = daka()
    timestamp = get_time_str()
    print(f'{timestamp}: {msg}')
```

try comment (1) and uncomment（2）to test if working properly