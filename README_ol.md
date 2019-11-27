# Project 10

## Django (Pair Programming)

### 데이터 베이스 설계

* Movie

  > genre와 1:N 관계이므로 ForeignKey 설정을 통해 연결을 해주게 됩니다.
  >
  > user 와 N:M 으로 연결하기 위하여 ManyToMany 필드를 이용하여 User 와 연결시켜 줍니다.

* Review

  > movie 와 1:N 관계로 ForeignKey 설정을 해주게 되고
  >
  > User와도 1:N 설정으로 ForeignKey 설정을 해줍니다.

### 2. Seed Data

> 예전에 사용했던 json 파일을 `movies/fixtures/` 디렉토리 생성후 옮긴 후

```bash
$ python manage.py loaddata genre.json
$ python manage.py loaddata movie.json
```

를 통하여 데이터를 만들어 줍니다.

### 3. `account` App

* forms.py

```python
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
```

> django.contrib.auth.forms 에서 기본적으로 등록되어있는 UserCreationForm을 가져와서 상속받아 CustomForm 을 만들어 줍니다.
>
> models.py 에 있는 User 모델을 가져와 사용하고 필드를 지정해서 폼을 만들어줍니다.

* views.py

```python
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login as auth_login
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/form.html', context)
```

> AuthenticationForm 을 불러와서 해당 폼을 채우고 유저를 받아서 로그인을 실행해 주게 된다.



```python
from .forms import CustomForm
def signup(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomForm()
    context ={'form':form}
    return render(request, 'accounts/form.html', context)
```

> CustomForm(CustomUserCreationForm) 을 가져와서 검증 후에 로그인을 시켜주고 인덱스로 넘겨주게 됩니다.



## 4. `Movies` App

```python
@require_POST
def review(request,movie_pk):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.movie = get_object_or_404(Movie,pk=movie_pk)
        review.user = request.user
        review.save()
        return redirect('movies:detail',movie_pk)
```

> ReviewForm은 Detail에서 넘겨주게 되고 review에선 @require_POST로 받아온 후 확인 절차를 거친뒤에 `form.save(commit=False)` 를 통해 review을 뽑아주고, 해당 영화와, user을 넣어 준후 다시 저장해줍니다.



```python
def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = get_object_or_404(Movie,pk=movie_pk)
            review.user = request.user
            review.save()
            return redirect('movies:detail',movie_pk)
    form = ReviewForm(instance=review)
    return render(request, 'accounts/form.html', {'form':form})
```

> review 생성과 동일한 방식으로 get요청일때는 instance에 review를 넣어서 넘겨주게 되고 POST 일때에는 commit = False를 통하여 movie, user 에 해당하는 정보를 넘겨주고 저장하게 됩니다.



* 좋아요

```python
@login_required
@require_POST
def like(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.user in movie.like_user.all():
        movie.like_user.remove(request.user)
    else:
        movie.like_user.add(request.user)
    return redirect('movies:detail',movie_pk)
```

>  해당 유저가 movie.like_user  ManyToMany 필드에 있는지 여부에 따라 remove 혹은 add를 통하여 like_user에 추가해 줍니다.