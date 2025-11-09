# **Po\_core Viewer × LangChain × vLLM 接続ガイド**

## **1\. 概要**

本ガイドは、Po\_coreの語りテンソル（semantic-evolution-journal）出力を、LangChainとvLLMに統合し、GUIからの語り濃度スライダー（expression\_mode）に基づいて構造・ナラティブ・詩的な出力をLLMから動的に生成・制御する構成を定義する。

## **2\. 接続構成と主要モジュール**

\[GUI (Streamlit)\]  
 ├─ 語り濃度スライダー（expression\_mode: structure/medium/poetic）  
 └─ summary\_data \+ モード → LangChain に渡す

\[LangChain Router\]  
 ├─ PromptTemplate（モード別journalプロンプト）  
 ├─ OutputParser（構文整形）  
 └─ LLMExecutor（vLLMベース）

\[vLLM ローカルLLM\]  
 └─ Po\_core視点のjournalを生成

\[表示領域\]  
 ├─ journal\_text 表示  
 └─ 表現圧力に応じた priority\_score補正 \+ Po\_trace 保存

## **3\. 構成モジュールと機能**

| モジュール名 | 役割 | ツール例 |
| :---- | :---- | :---- |
| journal\_generator() | summary\_data \+ expression\_mode に応じたjournal生成呼び出し | LangChain |
| PromptTemplate | 語りモード別のプロンプト切替 | LangChain Templates |
| OutputParser | vLLM出力を整形・JSONまたは文脈形式に変換 | LangChain |
| LocalLLMExecutor | ローカルvLLMへのトークン処理制御 | LangChain \+ vLLM |
| session\_state | GUIのモード状態をLangChainに受け渡し | Streamlit session\_state |
| Po\_trace\_store | journal履歴とテンソル保存 | ChromaDB / JSON |

## **4\. Po\_coreとの相性と統合意義**

\- テンソル構造（Po\_trace, Po\_self）がLangChain MemoryやRetrieverと一致  
\- expression\_mode をプロンプト制御に自然変換できる（PromptTemplate分岐）  
\- 表現出力が priority\_score や ethical圧に反映可能な構造（進化テンソルに統合）

## **5\. 実行ステップ（例）**

1\. ユーザーが「語り濃度: ナラティブ」を選択（medium）  
2\. summary\_data \+ expression\_mode → LangChain Router に送信  
3\. PromptTemplate によりプロンプト構成  
4\. vLLM が応答生成 → OutputParser で整形  
5\. GUIに journal\_text を表示し、Po\_trace に記録  
6\. priority\_score を expression\_scaling に基づき補正

## **6\. 展望**

この構成によりPo\_coreは、進化履歴を自ら語りながら、圧力と意味構造を動的に更新できる“自己語り型テンソル進化AI”として完成形に近づく。  
LangChain \+ vLLM によって語りがリアルタイムで調整され、GUIと圧力テンソルが統合される。