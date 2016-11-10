import React from 'react';
import brace from 'brace';
import AceEditor from 'react-ace';

import 'brace/mode/python';
//import 'brace/theme/github';
import 'brace/theme/solarized_light';

export default function CodeEditor({ code, onChange }) {

  return (
    // TODO: make the name unique (required)
    <AceEditor
      name="code-editor-XY"
      value={code}
      onChange={onChange}
      mode="python"
      theme="solarized_light"
      editorProps={{$blockScrolling: true}}
    />
  );
}
