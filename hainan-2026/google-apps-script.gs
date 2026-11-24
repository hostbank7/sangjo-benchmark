/**
 * 하이난 파크골프 국제오픈대회 참가 신청 접수용 Google Apps Script
 *
 * 하는 일
 *  1) 홈페이지에서 신청이 들어오면 이 스프레드시트의 '신청' 시트에 한 줄씩 기록
 *  2) 알림 메일을 NOTIFY_TO 주소(비어 있으면 스크립트 주인 Gmail)로 발송
 *
 * 설치 (5분)
 *  1) Google 드라이브에서 새 Google 스프레드시트를 만듭니다. (이름 예: 하이난 신청 접수)
 *  2) 확장 프로그램 > Apps Script 를 열고, 원래 있던 코드를 지운 뒤 이 파일 내용을 붙여넣고 저장합니다.
 *  3) 오른쪽 위 [배포] > [새 배포] > 톱니바퀴에서 '웹 앱' 선택
 *       - 실행 계정: 나
 *       - 액세스 권한: 모든 사용자
 *     [배포] 를 누르고 권한 요청이 나오면 허용합니다. ('안전하지 않음' 경고가 나오면 고급 > 이동)
 *  4) 나오는 '웹 앱 URL'(https://script.google.com/macros/s/..../exec)을 복사해 Claude 에게 알려 주세요.
 *     홈페이지 신청서가 이 주소로도 보내도록 연결해 드립니다.
 */

const SHEET_NAME = '신청';
const NOTIFY_TO = 'worldparkgolf77@gmail.com';

function doPost(e) {
  try {
    const d = JSON.parse((e.postData && e.postData.contents) || '{}');
    if (d._honey) return json_({ ok: true }); // 스팸 봇 차단

    const subject = String(d._subject || '[참가신청] 하이난 파크골프 국제오픈대회');
    const data = {};
    Object.keys(d).forEach(function (k) {
      if (k.charAt(0) === '_') return; // _subject, _captcha 같은 설정값은 빼고 저장
      data[k] = String(d[k] === null || d[k] === undefined ? '' : d[k]).slice(0, 2000);
    });

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    let headers = sh.getLastRow() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
    if (!headers.length) headers = ['접수 시각'];
    Object.keys(data).forEach(function (k) { if (headers.indexOf(k) < 0) headers.push(k); });
    sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');

    const row = headers.map(function (h) {
      if (h === '접수 시각') return new Date();
      const v = data[h] || '';
      return /^0\d/.test(v) ? "'" + v : v; // 전화번호 앞 0 유지
    });
    sh.appendRow(row);

    const body = Object.keys(data).map(function (k) { return k + ': ' + (data[k] || '-'); }).join('\n')
      + '\n\n신청 목록 보기: ' + ss.getUrl();
    MailApp.sendEmail({ to: NOTIFY_TO || Session.getEffectiveUser().getEmail(), subject: subject, body: body });

    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, message: '하이난 신청 접수 스크립트가 작동 중입니다.' });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
