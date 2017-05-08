var WeatherInstruments = React.createClass({
  // Function to load up the resources
  _loadWeatherData: function() {
    $.getJSON('/data/data.json', (response) => {
      this.setState({
        weatherData: response
      });
    });
  },

  // Initial state of the component with an empty array of resource
  getInitialState() {
    return { weatherData: [] }
  },
  // Function executed when the component just mounted
  componentDidMount() {
    this._loadWeatherData();
    setInterval(this._loadResources, 30000);
  },
  componentWillUnmount() {
    clearInterval(this.interval);
  },

  render() {
    return (
      // Return the instrument cluster
      <div className="row instrument-cluster">
        <Gauge data={this.state.weatherData}/>
      </div>
    );
  }
});

var Gauge = React.createClass({
  render: function() {
    return (
      <div className="col-md-3 gauge blue">
        <div className="instrument-name">Anemometer</div>
        <div className="latest-conditions">
          <div className="value">23</div>
          <div className="units">mph</div>
        </div>
        <h4>Current</h4>
      </div>
    );
  }
});

ReactDOM.render( <WeatherInstruments />, document.getElementById('weather-instruments') );
