var WeatherInstruments = React.createClass({
  // Function to load up the resources
  _loadWeatherData: function() {
    $.getJSON('./data/data.json', (response) => {
      this.setState({
        weatherData: response
      });
    });
  },

  // Initial state of the component with an empty array of resource
  getInitialState() {
    return {
      weatherData: {
        "current_conditions_metadata": {
          "timestamp": "2012-04-23T18:25:43.511Z",
          "wind_speed": 2.5,
          "wind_gusts": 10
        },
        "anemometer": {
          "speed": 0,
          "gusts": 0
        },
        "thermometer": {
          "current": 27
        },
        "hygrometer": {
          "relative_humidity": 0.4
        },
        "barometer": {
          "pressure": 29.92,
          "altitude": 3940
        }
      }
    }
  },
  // Function executed when the component just mounted
  componentDidMount() {
    this._loadWeatherData();
    setInterval(this._loadResources, 1000);
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
          <div className="value">{this.props.data.anemometer.speed}</div>
          <div className="units">m/s</div>
        </div>
        <h4>Current</h4>
      </div>
    );
  }
});

ReactDOM.render( <WeatherInstruments />, document.getElementById('weather-instruments') );
