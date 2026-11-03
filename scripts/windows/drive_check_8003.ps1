<#
.SYNOPSIS
  CHECK 8003 「데이터항목 검색」 화면을 읽기 전용으로 순회하고 상태별 캡처를 남긴다.

.DESCRIPTION
  CHECK Expert(checkxp.exe)는 관리자(HIGH) 무결성으로 실행되므로 일반 권한 프로세스의 마우스·키보드·윈도우
  메시지는 UIPI에 의해 조용히 무시된다. 이 스크립트는 반드시 "관리자 권한으로 실행"한 PowerShell에서 돌려야 한다.
  관리자가 아니면 아무것도 하지 않고 종료한다.

  하는 일(전부 읽기 전용):
    1. 8003 창이 열려 있는지 확인(열려 있지 않으면 종료)
    2. [기본] [상세] 탭 전환 캡처
    3. 함수 콤보, 조회주기 콤보를 열어서 캡처(항목은 고르지 않고 Esc로 닫음)
    4. 그리드 우클릭 메뉴를 열어서 캡처(항목은 누르지 않고 Esc로 닫음)
  하지 않는 일: 검색 실행 외의 조회 조건 변경, 엑셀로 보내기, 즐겨찾기 추가, 초기화, 어떤 저장·주문 버튼.

  캡처는 저장소 밖(%TEMP%\check8003)에만 쓴다. 캡처 원본은 공개 저장소에 올리지 않는다.
  실행 중에는 마우스와 키보드를 건드리지 않는다(사람 입력과 부딪히면 엉뚱한 곳을 누른다).

.EXAMPLE
  # 시작 메뉴에서 PowerShell을 우클릭 > 관리자 권한으로 실행한 뒤
  powershell -ExecutionPolicy Bypass -File .\scripts\windows\drive_check_8003.ps1
  powershell -ExecutionPolicy Bypass -File .\scripts\windows\drive_check_8003.ps1 -DryRun   # 계획만 출력
#>
param(
  [string]$OutDir = (Join-Path $env:TEMP 'check8003'),
  [int]$StepDelayMs = 1500,
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'

# --- 관리자 확인: 아니면 아무것도 하지 않는다 ---
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = (New-Object Security.Principal.WindowsPrincipal $id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
  Write-Host "관리자 권한이 아닙니다. CHECK(관리자 무결성)는 일반 권한의 입력을 무시하므로 아무것도 하지 않고 종료합니다." -ForegroundColor Yellow
  Write-Host "PowerShell을 '관리자 권한으로 실행'한 뒤 다시 실행하세요."
  exit 2
}

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class C8 {
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr p, CB cb, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetDlgCtrlID(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, int d, UIntPtr e);
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  [StructLayout(LayoutKind.Sequential)] public struct R { public int L, T, Rr, B; }
  public static R Rect(IntPtr root, int id) { R f = new R(); bool got = false;
    EnumChildWindows(root, (h, l) => { if (!got && GetDlgCtrlID(h) == id && IsWindowVisible(h)) { GetWindowRect(h, out f); got = true; } return true; }, IntPtr.Zero);
    if (!got) f.L = f.T = f.Rr = f.B = -1; return f; }
}
"@
[C8]::SetProcessDPIAware() | Out-Null

$chk = (Get-Process checkxp -ErrorAction SilentlyContinue | Select-Object -First 1)
if (-not $chk) { Write-Host "checkxp 프로세스가 없습니다. CHECK를 먼저 실행하고 8003 화면을 여세요." -ForegroundColor Yellow; exit 3 }
$hwnd = $chk.MainWindowHandle

# 8003 컨트롤(컨트롤 ID는 2026-11-03 관찰): 3=함수 콤보, 4=조회주기 콤보, 12=그리드, 14=기본/상세
$ctl = @{}
foreach ($id in 3, 4, 12, 14) { $ctl[$id] = [C8]::Rect($hwnd, $id) }
if ($ctl[14].L -lt 0) { Write-Host "8003 화면 컨트롤을 찾지 못했습니다. 8003 화면(데이터항목 검색)을 열어 두세요." -ForegroundColor Yellow; exit 4 }

function Center($r, $fx = 0.5, $fy = 0.5) { @([int]($r.L + ($r.Rr - $r.L) * $fx), [int]($r.T + ($r.B - $r.T) * $fy)) }
$plan = @(
  @{ name = '01_base';        act = 'capture' },
  @{ name = '02_detail_tab';  act = 'click';  pt = (Center $ctl[14] 0.75 0.5) },
  @{ name = '03_base_tab';    act = 'click';  pt = (Center $ctl[14] 0.25 0.5) },
  @{ name = '04_func_combo';  act = 'click';  pt = (Center $ctl[3]  0.5  0.5); then = 'esc' },
  @{ name = '05_cycle_combo'; act = 'click';  pt = (Center $ctl[4]  0.5  0.5); then = 'esc' },
  @{ name = '06_grid_rclick'; act = 'rclick'; pt = (Center $ctl[12] 0.5  0.25); then = 'esc' }
)
if ($DryRun) { $plan | ForEach-Object { "{0}: {1} {2}" -f $_.name, $_.act, ($_.pt -join ',') }; exit 0 }

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$W = [int](Get-CimInstance Win32_VideoController | Select-Object -First 1).CurrentHorizontalResolution
$H = [int](Get-CimInstance Win32_VideoController | Select-Object -First 1).CurrentVerticalResolution
function Shot($name) {
  $bmp = New-Object System.Drawing.Bitmap 1800, 950
  $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen(0, 0, 0, 0, $bmp.Size); $g.Dispose()
  $bmp.Save((Join-Path $OutDir "$name.png")); $bmp.Dispose(); Write-Host "캡처: $name"
}
function Click($pt, $right = $false) {
  [C8]::SetCursorPos($pt[0], $pt[1]) | Out-Null; Start-Sleep -Milliseconds 250
  $d = if ($right) { 8 } else { 2 }; $u = if ($right) { 16 } else { 4 }
  [C8]::mouse_event($d, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 80; [C8]::mouse_event($u, 0, 0, 0, [UIntPtr]::Zero)
}
function Esc { [C8]::keybd_event(0x1B, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 60; [C8]::keybd_event(0x1B, 0, 2, [UIntPtr]::Zero) }

[C8]::SetForegroundWindow($hwnd) | Out-Null; Start-Sleep -Milliseconds 1000
foreach ($s in $plan) {
  switch ($s.act) {
    'capture' { }
    'click'   { Click $s.pt }
    'rclick'  { Click $s.pt $true }
  }
  Start-Sleep -Milliseconds $StepDelayMs
  Shot $s.name
  if ($s.then -eq 'esc') { Esc; Start-Sleep -Milliseconds 600 }
}
Write-Host "완료. 캡처 폴더: $OutDir  (저장소에 올리지 말 것)" -ForegroundColor Green
