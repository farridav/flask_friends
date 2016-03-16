$('[href]').parent().removeClass('active');
$('[href="' + document.location.pathname + '"]').parent().addClass('active');

var Friend = React.createClass({
  render: function() {
      return (
      <li className="list-group-item">
          <img src={this.props.pic} />
          {this.props.name}
      </li>
    );
  }
});

var FriendBox = React.createClass({
  loadFriendsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
      return {
          'name': '',
          'friends': []
      };
  },
  componentDidMount: function() {
    this.loadFriendsFromServer();
    setInterval(this.loadFriendsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
        <FriendList data={this.state.friends} />
    );
  }
});

var FriendList = React.createClass({
  render: function() {
    var friendNodes = this.props.data.map(function(friend) {
      return (
        <Friend name={friend.name} pic={friend.picture.data.url} />
      );
    });
    return (
      <ul className="friendList">
        {friendNodes}
      </ul>
    );
  }
});

ReactDOM.render(
  <FriendBox url="/api/friends" pollInterval={10000} />,
  document.getElementById('friends')
);
