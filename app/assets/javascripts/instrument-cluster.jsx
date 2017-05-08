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
      </div>R
    );
  }
});

var Gauge = React.createClass({
  render: function() {
    return (
      <div class="col-md-3 gauge blue">
        <div class="instrument-name">Anemometer</div>
        <div class="latest-conditions">
          <div class="value">23</div>
          <div class="units">mph</div>
        </div>
        <h4>Current</h4>
      </div>
    );
  }
});

ReactDOM.render( <WeatherInstruments />, document.getElementById('weather-instruments') );
