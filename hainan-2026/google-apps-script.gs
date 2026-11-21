/**
 * 하이난 파크골프 국제오픈대회 참가 신청 접수용 Google Apps Script
 *
 * 하는 일
 *  1) 신청이 들어오면 이 스프레드시트의 '신청' 시트에 한 줄씩 기록
 *  2) 스크립트 주인(내 Gmail)에게 신청 알림 메일 발송
 *
 * 설치: Google 스프레드시트 > 확장 프로그램 > Apps Script 에 이 코드를 붙여넣고
 *       배포 > 새 배포 > 유형 '웹 앱' / 실행: 나 / 액세스: 모든 사용자 로 배포.
 */

const SHEET_NAME = '신청';
const HEADERS = ['접수 시각', '성명', '연락처', '참가 인원', '1인실', '동반자', '소속', '예상 참가비', '기타', '신청 페이지'];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents || '{}');
    if (d._honey) return json_({ ok: true }); // 스팸 봇 차단

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) sh.appendRow(HEADERS);

    const row = [new Date(), d.name, d.phone, d.count, d.single, d.companions, d.club, d.total, d.extra, d.page]
      .map(v => (v === undefined || v === null) ? '' : String(v).slice(0, 1000));
    // 전화번호가 숫자로 바뀌어 앞의 0이 사라지지 않도록 텍스트로 저장
    row[2] = "'" + row[2];
    sh.appendRow(row);

    const to = Session.getEffectiveUser().getEmail();
    const body = HEADERS.slice(1).map((h, i) => h + ': ' + (row[i + 1] || '-').toString().replace(/^'/, '')).join('\n')
      + '\n\n신청 목록: ' + ss.getUrl();
    MailApp.sendEmail({ to: to, subject: '[참가신청] ' + row[1] + ' ' + row[3] + ' · 하이난 파크골프 국제오픈대회', body: body });

    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, message: '신청 접수 서버가 작동 중입니다.' });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
