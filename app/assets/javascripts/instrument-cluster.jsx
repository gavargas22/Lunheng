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
          "wind_speed": 0,
          "wind_gusts": 0
        },
        "anemometer": {
          "speed": 0,
          "gusts": 0
        },
        "thermometer": {
          "current": 0
        },
        "hygrometer": {
          "relative_humidity": 0
        },
        "barometer": {
          "pressure": 0,
          "altitude": 0
        }
      }
    }
  },
  // Function executed when the component just mounted
  componentDidMount() {
    this._loadWeatherData();
    setInterval(this._loadWeatherData, 1000);
  },
  componentWillUnmount() {
    clearInterval(this.interval);
  },

  render() {
    return (
      // Return the instrument cluster
      <div>
        <Gauge data={this.state.weatherData}/>
      </div>
    );
  }
});

var Gauge = React.createClass({
  render: function() {
    return (
      <div className="row instrument-cluster">
        <div className="col-md-3 gauge blue">
          <div className="instrument-name">Anemometer</div>
          <div className="latest-conditions">
            <div className="value">{this.props.data.anemometer.speed}</div>
            <div className="units">m/s</div>
          </div>
          <h4>Current</h4>
        </div>
        <div className="col-md-3 gauge green">
          <div className="instrument-name">Thermometer</div>
          <div className="latest-conditions">
            <div className="value">{this.props.data.thermometer.outside}</div>
            <div className="units">°C</div>
          </div>
          <h4>Current</h4>
        </div>
      </div>
    );
  }
});

var UnitSelector = React.createClass({
  render: function() {
    return (
      <div className="unit-selector">
        <form>
          <div className="radio">
            <label>
              <input type="radio" value="metric" checked={true} />
              Metric
            </label>
          </div>
          <div className="radio">
            <label>
              <input type="radio" value="standard" />
              Standard
            </label>
          </div>
        </form>
      </div>
    );
  }
});

ReactDOM.render( <WeatherInstruments />, document.getElementById('weather-instruments') );
