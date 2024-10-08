# django blog project

 Django를 이용하여 실제로 사용 가능한 Blog를 만들어보자.
 본 프로젝트에서는 다양한 사람이 자신이 좋아하는 게임에 관련된 이야기를 할 수 있는 페이지를 만들어 보자.

## WBS
```mermaid
gantt
    title 블로그 프로젝트 일정
    dateFormat  YYYY-MM-DD
    section 0,1단계
    프로젝트 생성 및 초기 설정       :done, 2024-08-27, 1d
    Post, Category 모델 작성 :done, 2024-08-27, 1d
    Post List, Post Detail 템플릿 작성 :done, 2024-08-27, 1d
    Admin 페이지 설정                 :done, 2024-08-27, 1d

    section 1,2단계
    CRUD 기능 작성                  :done, 2024-08-28, 1d
    로그인/로그아웃/회원가입         :done, 2024-08-28, 1d
    검색 기능 구현                  :done, 2024-08-28, 1d
    블로그 방향성 수립             :done, 2024-08-28, 1d

    section 3단계
    게시물 댓글 기능 작성           :done, 2024-08-29, 1d
    게시물 사진 업로드 기능           :done, 2024-08-29, 1d
    회원 관련 추가 기능 작성        :done, 2024-08-29, 1d
    게시물 조회수 기능 구현          :done, 2024-08-29, 1d
    CBV 전환 도전                   :done, 2024-08-29, 3d

    section 프로젝트 완성단계
    백엔드 코드 마무리 및 통합 테스트 :done, 2024-08-30, 3d
    프론트엔드 코딩 - CSS 스타일링, UI 개선 :done, 2024-08-30, 3d
    리드미 작성 및 발표 준비          :done, 2024-08-30, 3d

    section 이후 블로그 배포 도전
    블로그 배포 도전                :done, 2024-08-31, 2d
```

## ERD

```mermaid
erDiagram
    User {
        int id PK
        string username
        string email
        string password
        string first_name(nickname)
    }
    
    Category {
        int id PK
        string name
    }

    Post {
        int id PK
        string title
        text content
        datetime created_date
        datetime updated_date
        int view_count
        string image
    }

    Comment {
        int id PK
        text message
        datetime created_at
        datetime updated_at
    }

    Tag {
        int id PK
        string name
    }

    User ||--o{ Post : "writes"
    User ||--o{ Comment : "writes"
    Category ||--o{ Post : "categorizes"
    Post ||--o{ Comment : "has"
    Post }o--|{ Tag : "tags"
```
## URLs

|html 위치   | URL Pattern                       | View Name               | Description                                        |
|---------|-----------------------------------|-------------------------|----------------------------------------------------|
|blog    | `/`                               | `HomeView`              | 메인 페이지                                         |
|         | `/post/`                          | `PostListView`          | 게시물 목록                                         |
|         | `/post/tag-search`                | `TagSearchView`         | 태그별 검색                                         |
|         | `/post/<int:pk>/`                 | `PostDetailView`        | 게시물 상세                                         |
|         | `/post/new/`                      | `PostCreateView`        | 게시물 작성                                         |
|         | `/post/<int:pk>/edit/`            | `PostEditView`          | 게시물 수정                                         |
|         | `/post/<int:pk>/delete/`          | `PostDeleteView`        | 게시물 삭제                                         |
|         | `/post/<int:pk>/comment_delete/`  | `CommentDeleteView`     | 댓글 삭제                                           |
|         | `/post-not-found/`                | `PostNotFoundView`      | 게시물을 찾을 수 없는 경우 표시                      |
|accounts| `/signup/`                        | `UserSignupView`        | 회원가입                                            |
|         | `/login/`                         | `UserLoginView`         | 로그인 페이지                                       |
|         | `/logout/`                        | `UserLogoutView`        | 로그아웃                                            |
|         | `/profile/`                       | `UserProfileView`       | 유저 프로필                                         |
|         | `/profile/update/`                | `UserProfileUpdateView` | 프로필 정보 수정                                    |
|         | `/profile/pass_update/`           | `UserPassUpdateView`    | 비밀번호 변경                                       |


## 기능
1. 게시물 관련
  - 게시물 목록
  - 게시물 상세
  - 게시물 수정 / 생성
  - 게시물 삭제
  - 게시물 댓글기능 / 댓글삭제
  - 태그별 검색기능
2. 계정 관련
  - 계정 생성 (회원가입)
  - 계정 프로필 확인
  - 계정 프로필 수정
  - 계정 비밀번호 변경

## 느낀점

- framework를 이용한다는것이 생각보다 그렇게 쉬운일은 아니었다.
- FBV -> CBV 바뀌는것은 예상외로 조정해야할 부분이 많이 있었다. 특히 View에 엮여있는 것이 많을수록.
- 막막하다고 멈춰있는 것 보단 뭐라도 해보는것이 나은 것 같다.
- 아! 이전 작업(tube clone)에서 accounts와 blog의 앱을 따로 분리한게 괜히하는게 아니구나!
