(require hyrule * :readers *)
(import toolz.itertoolz *)
(import pygls.lsp.types [CompletionItem
                         CompletionList
                         CompletionOptions
                         CompletionParams
                         CompletionItemKind
                         Hover
                         MarkupContent
                         MarkupKind])
(import hyuga.log *)
(import hyuga.sym.helper *)

(defn decide-kind
  [sym-type]
  "@see: https://docs.microsoft.com/en-us/dotnet/api/microsoft.visualstudio.languageserver.protocol.completionitemkind?view=visualstudiosdk-2022"
  (-> (branch (in it sym-type)
              "builtin" CompletionItemKind.Function
              ;; FIXME: pygls CompletionItemKind.Macro is not defined yet.
              ; "macro" 118115
              ; "macro" CompletionItemKind.Macro
              "macro" CompletionItemKind.Function
              "module" CompletionItemKind.Module
              "function" CompletionItemKind.Function
              "class" CompletionItemKind.Class
              else CompletionItemKind.Variable)
      int))

(defn create-item
  [prefix symdata]
  "TODO: doc"
  (logger.debug f"create-item symdata={symdata}")
  (let [prefix-splitted (.split prefix ".")
        sym-splitted (-> (:sym symdata) (.split "."))
        insert-text (if (module-or-class? prefix-splitted)
                      (-> sym-splitted last)
                      (:sym symdata))]
    (logger.debug (.format "insert-text={}" insert-text))
    (CompletionItem
      :label f"{(:sym symdata)} [{(:scope symdata)}]"
      :insert_text insert-text
      :detail (:docs symdata)
      :kind (decide-kind (str (:type symdata))))))

(defn create-items
  [prefix candidates]
  "TODO: doc"
  (logger.debug (.format "candidates={}" (repr candidates)))
  (->> candidates
       (map #%(create-item prefix %1))
       list))

(defn create-completion-list
  [items [is-incomplete False]]
  "TODO: doc"
  (CompletionList :is_incomplete is-incomplete
                  :items items))
