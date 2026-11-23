# 인스타그램 게시물 이미지 생성: python3 make_posts.py && node render.js ..
import pathlib
IMG = (pathlib.Path(__file__).resolve().parents[3] / 'img').as_uri() + '/'
OUT = pathlib.Path(__file__).resolve().parent.parent
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Noto Sans KR',sans-serif;color:#fff;background:#0f3a28;position:relative;word-break:keep-all}
.serif{font-family:'Noto Serif KR',serif}
.gold{color:#e8bd62}
.photo{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0}
.wrap{position:absolute;inset:0;padding:84px 80px;display:flex;flex-direction:column}
.kicker{font-size:30px;letter-spacing:6px;font-weight:700;color:#e8bd62}
.chip{display:inline-block;padding:10px 26px;border:2px solid #e8bd62;border-radius:40px;font-size:30px;font-weight:700;color:#e8bd62}
.foot{position:absolute;left:0;right:0;bottom:0;height:150px;background:#0b2a1d;display:flex;align-items:center;justify-content:space-between;padding:0 80px;border-top:3px solid #e8bd62}
.foot .l{font-size:34px;font-weight:700}
.foot .l small{display:block;font-size:24px;font-weight:500;color:#b9cbbf;margin-top:2px}
.foot .r{font-size:40px;font-weight:900;color:#e8bd62}
.page{position:absolute;top:60px;right:70px;font-size:26px;color:rgba(255,255,255,.75);font-weight:700}
.badge{display:inline-flex;align-items:center;gap:14px;background:rgba(0,0,0,.35);padding:12px 24px;border-radius:12px;font-size:28px;font-weight:700}
"""
FOOT = '<div class="foot"><div class="l">프로필 링크에서 신청<small>12월 10일 마감 · 150명 선착순</small></div><div class="r">☎ 010-5622-6576</div></div>'
def page(n): return f'<div class="page">{n} / 7</div>'

posts = {}
posts['01_초대'] = f"""
<div class="photo" style="background-image:url({IMG}hero.jpg);height:760px;bottom:auto;background-position:8% 50%"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 30%,rgba(15,58,40,0) 45%,#0f3a28 57%)"></div>
<div class="wrap" style="padding-bottom:180px">
  <div class="kicker">2026 · KOREA–CHINA INTERNATIONAL OPEN</div>
  <div style="flex:1"></div>
  <div class="serif" style="font-size:44px;font-weight:700;color:#e8bd62">하이난 미션힐스</div>
  <div class="serif" style="font-size:86px;font-weight:900;line-height:1.15;margin-top:6px">한·중 파크골프<br>국제오픈대회</div>
  <div style="font-size:32px;color:#cfe0d5;margin-top:22px">중국 국가체육총국 주최 · 하이난성 공식 후원</div>
  <div style="display:flex;gap:18px;margin-top:36px;flex-wrap:wrap">
    <span class="chip">12.27 ~ 1.1 · 4박 6일</span><span class="chip">티웨이 직항 전세기</span><span class="chip">1인 159만원</span>
  </div>
</div>{FOOT}"""

posts['02_상금'] = f"""
<div class="shade" style="background:radial-gradient(circle at 50% 38%,#1d5a40 0%,#0f3a28 55%,#0a2619 100%)"></div>
{page(2)}
<div class="wrap" style="align-items:center;text-align:center;padding-top:110px">
  <div class="kicker">PRIZE</div>
  <div style="font-size:46px;font-weight:700;margin-top:24px">우승하면</div>
  <div style="display:flex;align-items:flex-end;gap:10px;margin-top:6px">
    <span style="font-size:68px;font-weight:900;margin-bottom:46px">현금</span>
    <span class="serif gold" style="font-size:250px;font-weight:900;line-height:1">300</span>
    <span class="gold" style="font-size:80px;font-weight:900;margin-bottom:30px">만원</span></div>
  <div style="font-size:44px;font-weight:700;margin-top:24px">+ 하이난 투어 상품권 <span style="font-size:30px;color:#b9cbbf">(159만원 상당)</span></div>
  <div style="margin-top:36px;padding:20px 44px;background:#e8bd62;color:#0f3a28;border-radius:60px;font-size:46px;font-weight:900">총 459만원 상당</div>
  <div style="display:flex;gap:28px;margin-top:64px;width:100%">
    <div style="flex:1;border:2px solid rgba(232,189,98,.5);border-radius:20px;padding:30px 20px">
      <div class="gold" style="font-size:30px;font-weight:700">준우승</div>
      <div style="font-size:42px;font-weight:900;margin-top:8px">현금 200만원</div>
      <div style="font-size:28px;color:#cfe0d5;margin-top:6px">+ 프리미엄 파크골프채</div></div>
    <div style="flex:1;border:2px solid rgba(232,189,98,.5);border-radius:20px;padding:30px 20px">
      <div class="gold" style="font-size:30px;font-weight:700">참가자 전원</div>
      <div style="font-size:42px;font-weight:900;margin-top:8px">웰컴 선수팩</div>
      <div style="font-size:28px;color:#cfe0d5;margin-top:6px">공인구 · 모자 · 타월</div></div>
  </div>
</div>{FOOT}"""

posts['03_코스'] = f"""
<div class="photo" style="background-image:url({IMG}people.jpg);background-position:60% 50%"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 50%,rgba(8,30,20,.92) 78%)"></div>
{page(3)}
<div class="wrap" style="padding-bottom:180px">
  <div class="kicker">COURSE</div>
  <div class="serif" style="font-size:64px;font-weight:900;margin-top:14px;text-shadow:0 2px 12px rgba(0,0,0,.5)">연평균 24℃,<br>겨울에도 초록 잔디</div>
  <div style="flex:1"></div>
  <div style="font-size:40px;font-weight:700">하이난 미션힐스 리조트 안 파크골프장</div>
  <div style="font-size:31px;color:#d6e4db;margin-top:12px;line-height:1.5">숙소에서 도보·카트로 바로 이동<br>공식 연습 18 + 본선 36 + 친선전 18 + 굿바이 18</div>
  <div style="margin-top:26px"><span class="chip" style="font-size:40px;background:rgba(0,0,0,.3)">총 90홀 라운딩</span></div>
</div>{FOOT}"""

items = [('✈️','티웨이 인천 직항 전세기 왕복'),('🏨','5성급 미션힐스 리조트 4박'),('🍽️','전 일정 식사 · 환영만찬 · 갈라디너'),('⛳','대회 참가비 · 그린피 · 락카 (90홀)'),('♨️','천연 화산암 온천 무제한'),('🚌','전용 차량 · 한국어 가이드'),('🛍️','하이커우 문화 투어 · 면세점 VIP'),('🛂','중국 무비자 입국 (비자비 없음)')]
li = ''.join(f'<div style="display:flex;align-items:center;gap:22px;padding:17px 0;border-bottom:1px solid rgba(255,255,255,.14);font-size:35px;font-weight:500"><span style="font-size:38px;width:50px;text-align:center">{e}</span>{t}</div>' for e,t in items)
posts['04_포함내역'] = f"""
{page(4)}
<div class="wrap" style="padding-bottom:180px">
  <div class="kicker">ALL INCLUSIVE</div>
  <div style="display:flex;align-items:baseline;gap:16px;margin-top:18px">
    <span style="font-size:48px;font-weight:700">1인</span>
    <span class="serif gold" style="font-size:150px;font-weight:900;line-height:1">159</span>
    <span class="gold" style="font-size:60px;font-weight:900">만원</span>
    <span style="font-size:30px;color:#b9cbbf;margin-left:8px">2인 1실</span></div>
  <div style="font-size:32px;color:#cfe0d5;margin-top:14px">하루 약 26.5만원으로 모두 포함</div>
  <div style="margin-top:30px">{li}</div>
  <div style="font-size:25px;color:#9fb3a7;margin-top:22px">현지 미팅·샌딩 $50 별도 · 1인실 1박 10만원 추가</div>
</div>{FOOT}"""

days=[('12/27 일','인천 출발 (21:30 전세기) → 하이커우 도착'),('12/28 월','선수 등록 · 연습 18홀 · 한·중 우호의 밤'),('12/29 화','개막식 · 본선 36홀 스트로크'),('12/30 수','한·중 친선전 · 문화 투어 · 시상 갈라디너'),('12/31 목','굿바이 라운딩 · 면세점 · 송년 만찬'),('1/1 금','새해 첫날 인천 도착 (06:45)')]
dl=''.join(f'<div style="display:flex;gap:26px;align-items:flex-start;padding:20px 0;border-bottom:1px solid rgba(255,255,255,.14)"><div style="min-width:118px;padding:6px 0;background:{"#e8bd62" if i in (2,3) else "rgba(232,189,98,.16)"};color:{"#0f3a28" if i in (2,3) else "#e8bd62"};border-radius:10px;text-align:center;font-size:26px;font-weight:900">{i+1}일차</div><div><div style="font-size:26px;color:#b9cbbf;font-weight:700">{d}</div><div style="font-size:34px;font-weight:700;margin-top:2px">{t}</div></div></div>' for i,(d,t) in enumerate(days))
posts['05_일정'] = f"""
<div class="photo" style="background-image:url({IMG}onsen.jpg);height:300px;bottom:auto"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(15,58,40,.2) 0%,rgba(15,58,40,.6) 14%,#0f3a28 23%)"></div>
{page(5)}
<div class="wrap" style="padding-bottom:180px">
  <div class="kicker">ITINERARY</div>
  <div class="serif" style="font-size:66px;font-weight:900;margin-top:10px">4박 6일 일정</div>
  <div style="font-size:30px;color:#cfe0d5;margin-top:8px">숙소 이동 없는 5성급 원스톱 · 송년과 새해를 하이난에서</div>
  <div style="margin-top:22px">{dl}</div>
</div>{FOOT}"""

safe=[('공식 대회','중국 국가체육총국 주최 · 하이난성 공식 후원'),('등록 여행사 계약','주식회사 투어유니버스 (717-86-03318)'),('법인 계좌로만 입금','우리은행 · 예금주 주식회사 투어유니버스'),('항공편 공개','티웨이 TW9623 / TW9624 전세기'),('표준약관 · 환불 규정','공정거래위원회 여행업 표준약관'),('출발 7일 전 확정 통지','최소 100명 충족 여부 사전 안내')]
sl=''.join(f'<div style="display:flex;gap:24px;align-items:center;background:rgba(255,255,255,.06);border-radius:18px;padding:17px 28px;margin-bottom:13px"><div style="width:58px;height:58px;border-radius:50%;background:#e8bd62;color:#0f3a28;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;flex:none">✓</div><div><div style="font-size:36px;font-weight:900">{a}</div><div style="font-size:27px;color:#cfe0d5;margin-top:2px">{b}</div></div></div>' for a,b in safe)
posts['06_안심정보'] = f"""
{page(6)}
<div class="wrap" style="padding-bottom:180px">
  <div class="kicker">SAFE</div>
  <div class="serif" style="font-size:66px;font-weight:900;margin-top:10px">안심하고 신청하세요</div>
  <div style="font-size:30px;color:#cfe0d5;margin-top:10px;margin-bottom:26px">확인할 수 있는 정보를 모두 공개합니다</div>
  {sl}
</div>{FOOT}"""

posts['07_마감임박'] = f"""
<div class="photo" style="background-image:url({IMG}main.jpg);background-position:30% 50%"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(8,30,20,.55) 0%,rgba(8,30,20,.85) 45%,rgba(8,30,20,.96) 100%)"></div>
{page(7)}
<div class="wrap" style="align-items:center;text-align:center;padding-top:130px;padding-bottom:180px">
  <div class="kicker">LAST CALL</div>
  <div class="serif" style="font-size:76px;font-weight:900;margin-top:24px">신청 마감 임박</div>
  <div style="margin-top:40px;background:#e8bd62;color:#0f3a28;border-radius:28px;padding:30px 60px">
    <div style="font-size:34px;font-weight:700">신청 마감</div>
    <div class="serif" style="font-size:120px;font-weight:900;line-height:1.1">12월 10일</div>
    <div style="font-size:32px;font-weight:700">목요일 · 좌석이 차면 조기 마감</div></div>
  <div style="font-size:40px;font-weight:700;margin-top:46px">전세기 150석 선착순</div>
  <div style="font-size:31px;color:#cfe0d5;margin-top:14px;line-height:1.55">12.27 ~ 1.1 · 1인 159만원<br>우승 현금 300만원 + 투어 상품권</div>
  <div style="flex:1"></div>
  <div style="font-size:34px;font-weight:700">신청은 <span class="gold">프로필 링크</span> 또는 <span class="gold">댓글 "하이난"</span></div>
</div>{FOOT}"""


for name, body in posts.items():
    (OUT / f'_{name}.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
