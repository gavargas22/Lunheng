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
        "timestamp": "",
        "anemometer": {
          "speed": 0,
          "gusts": 0
        },
        "thermometer": {
          "outside": 0
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
    setInterval(this._loadWeatherData, 5000);
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

var parseDate = function(dateobject) {
  var readableDate = new Date(dateobject).toDateString()
  return readableDate
}

var Gauge = React.createClass({
  // Function to convert to certain units
  _convertToSelectedSpeedUnits: function(units, speed_in_mps) {
    var converted_speed = 0.0
    if (units == "mph") {
      converted_speed = Number((parseFloat(speed_in_mps) * (3600 * 0.000621371)).toFixed(1)
    }
    return converted_speed
  },

  _returnCalculationStatement: function() {
    return (
      <h1>Hello World!</h1>
    );
  },

  render: function() {
    return (
      // <div className="container">
      //   <div className="unit-selector">
      //     <div className="btn-group" role="group">
      //       <button type="button" className="btn btn-default" id="metric" onClick={this._convertToSelectedSpeedUnits}>Metric</button>
      //       <button type="button" className="btn btn-default" id="english" onClick={this._convertToSelectedSpeedUnits}>English</button>
      //       <button type="button" className="btn btn-default" id="raw" onClick={this._convertToSelectedSpeedUnits}>Raw</button>
      //     </div>
      //   </div>
      // </div>

      <div className="row instrument-cluster">
        <h2 className="timestamp">Conditions at: {this.props.data.timestamp}</h2>
        <div className="col-md-3 gauge blue">
          <div className="instrument-name">Anemometer</div>
          <div className="latest-conditions">
            <div className="value">{this._convertToSelectedSpeedUnits("mph", this.props.data.anemometer.speed)}</div>
            <div className="units">mph</div>
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

ReactDOM.render( <WeatherInstruments />, document.getElementById('weather-instruments') );
