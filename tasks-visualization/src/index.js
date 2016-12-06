import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { Provider } from 'react-redux';
import { CodeEditorContainer, SpaceGameContainer } from 'flocs-visual-components';
import { flocsComponentsReducer, flocsActionCreators } from 'flocs-visual-components';
import { flocsActions } from 'flocs-visual-components';


function createTaskAppComponent() {
  const rootReducer = combineReducers({
    myApp: myAppReducer,
    flocsComponents: flocsComponentsReducer
  });

  const middleware = applyMiddleware(thunk);
  const store = createStore(rootReducer, middleware);


  const task = {
    setting: {
      fields: [[["b", []], ["b", ["A"]], ["b", ["M"]], ["b", ["A"]], ["b", []]], [["k", []], ["k", ["A"]], ["k", []], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", ["M"]], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", []], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", ["M"]], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", []], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", ["M"]], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", []], ["k", ["A"]], ["k", []]], [["k", []], ["k", ["A"]], ["k", ["S"]], ["k", ["A"]], ["k", []]]],
    }
  };
  const taskEnvId = "single";
  store.dispatch(flocsActionCreators.setTask(taskEnvId, task));

  const appComponent = (
    <Provider store={store}>
      <div>
        <SpaceGameContainer taskEnvironmentId={taskEnvId}/>
        <CodeEditorContainer taskEnvironmentId={taskEnvId}/>
      </div>
    </Provider>
  );
  return appComponent;
}

function myAppReducer(state={}, action) {
  switch (action.type) {
    case flocsActions.SET_TASK:
      console.log('myAppReducer responding to new task:', action.payload);
      return state;
    case flocsActions.TASK_ATTEMPTED:
      console.log('myAppReducer responding to attempted task:', action.payload);
      return state;
    default:
      return state;
  }
}


const mountElement = document.getElementById('flocsTasksApp');
const appComponent = createTaskAppComponent();
ReactDOM.render(appComponent, mountElement);
