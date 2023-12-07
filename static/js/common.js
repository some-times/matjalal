
function checkLoginStatus() {
    fetch('/api/check_login_status', {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            const loginSignupElement = document.getElementById('logout')
            const logoutElement = document.getElementById('login-signup')

            if (data.isLoggedIn) {
                loginSignupElement.style.display = 'inline-block'
                logoutElement.style.display = 'none';
            } else {
                loginSignupElement.style.display = 'none'
                logoutElement.style.display = 'inline-block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 로그인 유효성 검사
async function validateLogin() {

    let id = document.getElementById('id').value.trim()
    let password = document.getElementById('password').value.trim()

    if (id === '' || password === '') {
        alert('아이디또는 비밀번호를 입력해주세요')
        return false
    }

    const response = await fetch('/api/check_password', {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'id': id,
            'password': password,
        }),
    })
    
    const result = await response.json()

    if(!result.isValid) {
        document.getElementById('passwordMismatch').innerText = '아이디 또는 비밀번호가 올바르지 않습니다.'
        document.getElementById('passwordMismatch').style.display = 'block'
        return false
    } else {
        document.getElementById('passwordMismatch').style.display = 'none'
        return true
    }
    
}

// 회원가입 유효성 검사
function validateJoin() {
    let username = document.getElementById('username')
    let userId = document.getElementById('userId')
    let password = document.getElementById('userPassword')
    let confirmPassword = document.getElementById('confirmPassword')
    let isValid = true

    if (username.value == "") {
        alert("이름을 작성해주세요.")
        username.focus()
        return false
    }

    if (userId.value.length < 4) {
        alert("아이디는 4글자 이상으로 작성해주세요.")
        userId.focus()
        return false
    }

    if (password.value == "") {
        alert("비밀번호를 작성해주세요.")
        return false
    }

    if (password.value != confirmPassword.value) {
        alert('비밀번호가 동일하지 않습니다.')
        confirmPassword.focus()
        return false
    }

    return isValid
}

// 아이디 동일성 체크
function checkDuplicateId() {
    
    let userId = document.getElementById('userId').value

    fetch('/api/check_duplicate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: userId }),
    })
    .then(res => res.json())
    .then(data => {
        if(data.isDuplicate) {
            alert("이미 사용 중인 아이디입니다.")
            document.getElementById('userId').value=''
            document.getElementById('userId').focus()
        }
    })
    .catch(error => {
        console.log('Error', error)
    })
}

// 비밀번호 동일성 체크

