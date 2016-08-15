import { connect } from 'react-redux';
import Main from '../components/Main';


function mapStateToProps(state, props) {
  return {
    path: extractPathPartsFromProps(props),
  };
}


function extractPathPartsFromProps(props) {
  // TODO: generalize
  const path = props.location.pathname;
  if (path.startsWith('/tasks')) {
    if (props.params.taskId) {
      return ['home', 'tasks', props.params.taskId];
    }
    return ['home', 'tasks'];
  }
  return ['home'];
}


function mapDispatchToProps(dispatch) {
  return {};  // TBA
}


const MainContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Main);

export default MainContainer;
