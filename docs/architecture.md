# アーキテクチャ設計

## 命名規則
|項目|規則|例|
|----|----|----|
|ファイル名|スネーク|example_file|
|クラス名|パスカル|ExampleClass|


## アーキテクチャ
```mermaid
flowchart LR
    A[User] ---
    B[View/Mapper] ---
    C[ViewControl] ---
    D[UseCase] ---
    E[WebControl/Mapper] ---
    F[Web]
```
