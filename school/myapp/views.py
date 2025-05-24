from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def login(request):
    return render(request, 'login.html', locals())

# 假設你已經有一個用戶模型或某種方式來驗證用戶
# 這裡我們用一個簡化的字典來模擬用戶資料

# 假設的用戶資料 (實際應用中會從資料庫查詢)
MOCK_USERS = {
    'teacher_user': {'password': 'teacher_pass', 'role': 'teacher', 'name': '王小明'},
    'student_user': {'password': 'student_pass', 'role': 'student', 'name': '陳大華'},
    # 可以添加更多用戶...
}

def login_view(request):
    """
    處理登入表單提交的視圖。
    - 接收 POST 請求。
    - 驗證帳號、密碼和身份。
    - 根據身份重定向到相應的頁面。
    - 如果是 GET 請求，則顯示登入頁面。
    """
    if request.method == 'POST':
        # 從表單獲取數據
        username = request.POST.get('usernameInput')
        password = request.POST.get('passwordInput')
        selected_role = request.POST.get('roleSelect') # 來自下拉選單

        # 簡單的用戶驗證邏輯
        user_data = MOCK_USERS.get(username)

        if user_data and user_data['password'] == password:
            # 檢查選擇的身份是否與用戶資料中的身份匹配
            if user_data['role'] == selected_role:
                # 登入成功，根據身份進行重定向
                if selected_role == 'teacher':
                    # 重定向到教職員首頁
                    # 可以在這裡將用戶姓名儲存到 session 中，以便 teacherHome.html 顯示
                    request.session['user_name'] = user_data['name']
                    return redirect('teacherHome') # 使用命名 URL 'teacher_home'
                elif selected_role == 'student':
                    # 重定向到學生首頁
                    # 同樣，儲存姓名到 session
                    request.session['user_name'] = user_data['name']
                    return redirect('studentHome') # 使用命名 URL 'student_home'
                else:
                    # 未知的身份選擇，返回登入頁面並顯示錯誤
                    return render(request, 'login.html', {'error': '選擇的身份無效。'})
            else:
                # 選擇的身份與用戶資料不符
                return render(request, 'login.html', {'error': '選擇的身份與帳號不符。'})
        else:
            # 帳號或密碼錯誤
            return render(request, 'login.html', {'error': '帳號或密碼錯誤。'})

    # 如果是 GET 請求，顯示登入頁面
    return render(request, 'login.html')

# 以下是教職員和學生的首頁視圖，它們會渲染對應的 HTML 檔案
def teacherHome(request):
    # 從 session 獲取用戶名，如果沒有則使用預設值
    user_name = request.session.get('user_name', '教職員')
    return render(request, 'teacherHome.html', {'user_name': user_name})

def studentHome(request):
    # 從 session 獲取用戶名，如果沒有則使用預設值
    user_name = request.session.get('user_name', '學生')
    return render(request, 'studentHome.html', {'user_name': user_name})
