(require hyrule * :readers *)
(import hyrule.misc *)

(import toolz.itertoolz *)
(import pygls.lsp.types [CompletionItem
                         CompletionList
                         CompletionOptions
                         CompletionParams
                         CompletionItemKind
                         Hover
                         Range
                         Location
                         Position
                         MarkupContent
                         MarkupKind])

(import hyuga.log *)
(import hyuga.api *)
(import hyuga.sym.helper *)

(defn decide-kind
  [sym-type]
  "@see: https://docs.microsoft.com/en-us/dotnet/api/microsoft.visualstudio.languageserver.protocol.completionitemkind?view=visualstudiosdk-2022"
  (-> (branch (in it sym-type)
              "builtin" CompletionItemKind.Function
              ;; FIXME: pygls CompletionItemKind.Macro is not defined yet.
              ; "macro" 118115
              ; "macro" CompletionItemKind.Macro
              "hy-special" CompletionItemKind.Keyword
              "hy-macro" CompletionItemKind.Keyword
              "macro" CompletionItemKind.Function
              "module" CompletionItemKind.Module
              "function" CompletionItemKind.Function
              "class" CompletionItemKind.Class
              else CompletionItemKind.Variable)
      int))

(defn create-item
  [word symdata]
  "TODO: doc"
  (logger.debug f"create-item symdata={symdata}")
  (let+ [{symkey "sym" docs "docs" typev "type"} symdata
         prefix-splitted (.split word ".")
         [scope full-sym] (get-scope/ns symkey)
         [ns sym] (get-ns/sym full-sym)
         insert-text (if (module-or-class? prefix-splitted)
                       sym
                       sym)]
    (CompletionItem
      :label f"{sym}\t[{scope}]\t<{full-sym}>"
      :insert_text insert-text
      :detail docs
      :kind (decide-kind (str typev)))))

(defn create-items
  [word]
  "TODO: doc"
  (->> (get-candidates word)
       (map #%(create-item word %1))
       list))

(defn create-completion-list
  [items [is-incomplete False]]
  "TODO: doc"
  (CompletionList :is_incomplete is-incomplete
                  :items items))

(defn create-hover
  [docs]
  (Hover
    :contents (MarkupContent
                :kind MarkupKind.PlainText
                :value docs)))

(defn create-location
  [pos uri]
  "TODO: doc"
  (let [obj-pos (Position :line (-> pos first dec)
                          :character (-> pos second dec))
        obj-range (Range :start obj-pos
                         :end obj-pos)]
    (Location :uri uri
              :range obj-range)))

(defn create-location-list
  [sym/vals]
  "TODO: doc"
  (->> sym/vals
       (map #%(let+ [{pos "pos" uri "uri"} (second %1)]
                (when (and pos uri)
                  (create-location pos uri))))
       (filter #%(is-not %1 None))
       list))
