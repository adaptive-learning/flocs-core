import { connect } from 'react-redux';
import Main from '../components/Main';


const mapStateToProps = (state) => {
  return {
    task: state.task
  };
};


const mapDispatchToProps = (dispatch) => {
  return {};  // TBA
};

const MainContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Main);

export default MainContainer;
