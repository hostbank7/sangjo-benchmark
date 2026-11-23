/**
 * 파크골프협회 협조요청 공문 메일 자동 발송 (Google Apps Script)
 *
 * 하는 일
 *  - '협회 연락처' 시트에서 [이메일 있음 + 전화 연락일 있음 + 메일 발송일 비어 있음] 인 협회에만
 *    협회 이름을 넣은 맞춤 메일과 공문 PDF를 한 통씩 보내고, '메일 발송일'에 날짜를 적습니다.
 *  - 전화로 먼저 인사하고 메일을 받아도 된다고 한 곳에만 보내도록 '전화 연락일'을 조건으로 둡니다.
 *    (정보통신망법상 광고성 메일은 받는 쪽 동의가 필요합니다. 전화 연락일을 적는 것이 그 기록입니다.)
 *  - 홈페이지 주소에 협회별 추천 코드(?ref=협회-지역)를 붙여, 신청서에 어느 협회를 통해 왔는지 남습니다.
 *
 * 설치
 *  1) 파크골프협회_연락처_관리표.xlsx 를 Google 드라이브에 올리고 'Google 스프레드시트로 열기'
 *     (파일 > Google 스프레드시트로 저장).
 *  2) 협조요청_공문_팸플릿포함.pdf 를 드라이브에 올리고, 파일 주소의 /d/ 와 /view 사이 글자를
 *     아래 ATTACH_FILE_ID 에 붙여넣기.
 *  3) 스프레드시트 > 확장 프로그램 > Apps Script 에 이 코드를 붙여넣고 저장.
 *  4) 스프레드시트를 새로고침하면 위쪽에 '홍보 메일' 메뉴가 생깁니다.
 *     먼저 '① 나에게 테스트 발송'으로 메일 모양을 확인한 다음 '② 협회에 발송'을 누르세요.
 */

const SHEET = '협회 연락처';
const ATTACH_FILE_ID = '여기에_공문_PDF_파일_ID';
const SENDER_NAME = 'WP 월드파크골프 고용호 고문이사';
const PAGE_URL = 'https://hostbank7.github.io/sangjo-benchmark/hainan-2026/';
const PHONE = '010-5622-6576';
const MAX_PER_RUN = 40; // 개인 Gmail 하루 발송 한도(약 100통)보다 넉넉히 낮게

// 열 번호 (A=1)
const COL = { region: 2, name: 3, email: 5, called: 8, sent: 9, reply: 10 };

function onOpen() {
  SpreadsheetApp.getUi().createMenu('홍보 메일')
    .addItem('① 나에게 테스트 발송', 'sendTest')
    .addItem('② 협회에 발송 (전화 연락한 곳만)', 'sendToAssociations')
    .addToUi();
}

function buildMail_(assoc, region) {
  const ref = encodeURIComponent('협회-' + region);
  const link = PAGE_URL + '?ref=' + ref;
  const subject = '[협조 요청] 2026 하이난 미션힐스 한·중 파크골프 국제오픈대회 회원 안내 부탁드립니다 (' + assoc + ')';
  const html =
    '<div style="font-family:sans-serif;font-size:15px;line-height:1.7;color:#222">' +
    '<p>' + assoc + ' 관계자님께,</p>' +
    '<p>얼마 전 전화로 인사드린 WP 월드파크골프 고용호 고문이사입니다. 말씀드린 대로 공문과 안내 자료를 보내 드립니다.</p>' +
    '<p>중국 국가체육총국이 주최하고 하이난성이 공식 후원하는 <b>「2026 하이난 미션힐스 한·중 파크골프 국제오픈대회」</b>에 ' +
    '한국 파크골프 동호인을 초대하고자 합니다. 회원님들께 안내해 주시면 감사하겠습니다.</p>' +
    '<ul>' +
    '<li>기간: 2026년 12월 27일(일) ~ 2027년 1월 1일(금), 4박 6일</li>' +
    '<li>항공: 티웨이항공 인천 ↔ 하이커우 직항 전세기</li>' +
    '<li>참가비: 1인 159만원 (항공·5성급 숙박·전 일정 식사·그린피 포함)</li>' +
    '<li>시상: 우승 현금 300만원 + 투어 상품권, 준우승 현금 200만원</li>' +
    '<li>모집: 150명 선착순 · <b>신청 마감 12월 10일(목)</b></li>' +
    '</ul>' +
    '<p>자세한 안내와 신청: <a href="' + link + '">' + link + '</a><br>' +
    '(회원님들이 이 주소로 신청하시면 ' + assoc + ' 소속으로 확인됩니다.)</p>' +
    '<p>단체로 참가하시는 경우 따로 상담해 드립니다. 문의: ' + PHONE + '</p>' +
    '<p>감사합니다.<br>' + SENDER_NAME + ' 드림<br>' +
    '여행 주관: 주식회사 투어유니버스 (사업자등록번호 717-86-03318)</p>' +
    '<p style="font-size:12px;color:#888">이 메일은 전화로 수신에 동의해 주신 곳에만 보내 드렸습니다. ' +
    '더 받지 않으시려면 이 메일에 "수신거부"라고 답장해 주세요.</p>' +
    '</div>';
  return { subject: subject, html: html };
}

function attachments_() {
  try { return [DriveApp.getFileById(ATTACH_FILE_ID).getBlob()]; }
  catch (e) { throw new Error('공문 PDF를 찾지 못했습니다. ATTACH_FILE_ID 를 확인하세요.'); }
}

function sendTest() {
  const me = Session.getEffectiveUser().getEmail();
  const m = buildMail_('서울 파크골프협회', '서울');
  MailApp.sendEmail({ to: me, subject: '[테스트] ' + m.subject, htmlBody: m.html, name: SENDER_NAME, attachments: attachments_() });
  SpreadsheetApp.getUi().alert(me + ' 로 테스트 메일을 보냈습니다. 받은편지함을 확인하세요.');
}

function sendToAssociations() {
  const ui = SpreadsheetApp.getUi();
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET);
  const rows = sh.getRange(2, 1, sh.getLastRow() - 1, 12).getValues();

  const targets = [];
  rows.forEach(function (r, i) {
    const email = String(r[COL.email - 1]).trim();
    const called = r[COL.called - 1];
    const sent = r[COL.sent - 1];
    const reply = String(r[COL.reply - 1]);
    if (email && called && !sent && reply !== '거절' && /@/.test(email)) targets.push(i);
  });

  if (!targets.length) {
    ui.alert('보낼 곳이 없습니다.\n이메일과 "전화 연락일"이 적혀 있고 "메일 발송일"이 비어 있는 협회에만 보냅니다.');
    return;
  }
  const n = Math.min(targets.length, MAX_PER_RUN, MailApp.getRemainingDailyQuota());
  if (ui.alert(n + '곳에 공문 메일을 보낼까요?', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;

  const files = attachments_();
  let done = 0;
  for (let k = 0; k < n; k++) {
    const i = targets[k];
    const r = rows[i];
    const m = buildMail_(r[COL.name - 1], r[COL.region - 1]);
    try {
      MailApp.sendEmail({ to: String(r[COL.email - 1]).trim(), subject: m.subject, htmlBody: m.html, name: SENDER_NAME, attachments: files });
      sh.getRange(i + 2, COL.sent).setValue(new Date());
      sh.getRange(i + 2, COL.reply).setValue('대기');
      done++;
      Utilities.sleep(1500); // 한꺼번에 몰아 보내지 않도록 간격
    } catch (e) {
      sh.getRange(i + 2, 12).setValue('발송 실패: ' + e);
    }
  }
  ui.alert(done + '곳에 보냈습니다.' + (targets.length > n ? '\n남은 ' + (targets.length - n) + '곳은 내일 다시 누르세요.' : ''));
}
