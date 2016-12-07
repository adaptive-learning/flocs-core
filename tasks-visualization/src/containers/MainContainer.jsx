import { connect } from 'react-redux';
import Main from '../components/Main';


function mapStateToProps(state, props) {
  return props;
};


const MainContainer = connect(mapStateToProps)(Main);

export default MainContainer;
