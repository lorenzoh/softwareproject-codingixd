let DATA = {
  "lastNSeconds": 30,
  "regions": {
      "cart1": {
          "id": "cart1",
          "n": 4,
          "max": 8,
          "entered": 5,
          "exited": 4
      },
      "cart2": {
          "id": "cart2",
          "n": 5,
          "max": 8,
          "entered": 4,
          "exited": 6
      },
      "cart3": {
          "id": "cart3",
          "n": 0,
          "max": 8,
          "entered": 0,
          "exited": 6
      }
  }
}

class Dash extends React.Component {
  constructor(props) {
    super(props);
    this.state= {
      lastNSeconds: DATA.lastNSeconds,
      regions: DATA.regions,
    }
  this.update = this.update.bind(this);
  }
  
  update() {
    let DATA = {
      "lastNSeconds": 300,
      "regions": {
          "cart1": {
              "id": "cart1",
              "n": 0,
              "max": 813,
              "entered": 531,
              "exited": 412
          },
          "cart2": {
              "id": "cart2",
              "n": 531,
              "max": 823,
              "entered": 431,
              "exited": 6123
          },
          "cart3": {
              "id": "cart3",
              "n": 123,
              "max": 8342,
              "entered": 53,
              "exited": 653
          }
      }
    }
    this.setState({
      regions: DATA.regions,
    })
  }

  //componentDidMount() {
  //  document.getElementById("bar").animate([
  //    {width: '100%'},
  //    {width: '0%'}
  //  ],{
  //    duration: this.state.intervallLenght *1000,
  //    iterations: Infinity,
  //    easing: "linear"
  //  })
  //}

  render() {
    console.log(this.state.carts)
    return(
      <div className="mom" >
        <div className="train">
          <Cart {...this.state.regions.cart1} />
          <Cart {...this.state.regions.cart2} />
          <Cart {...this.state.regions.cart3} />
        </div>
        <div onClick={this.update()} >click</div>
        <div id="description">
          Number of People who entered (<svg className="arrow arrow-up" viewBox="0 0 512.171 512.171">
            <path d="M479.046,283.925c-1.664-3.989-5.547-6.592-9.856-6.592H352.305V10.667C352.305,4.779,347.526,0,341.638,0H170.971
            c-5.888,0-10.667,4.779-10.667,10.667v266.667H42.971c-4.309,0-8.192,2.603-9.856,6.571c-1.643,3.989-0.747,8.576,2.304,11.627
            l212.8,213.504c2.005,2.005,4.715,3.136,7.552,3.136s5.547-1.131,7.552-3.115l213.419-213.504
            C479.793,292.501,480.71,287.915,479.046,283.925z"/>
          </svg>) and exited (<svg className="arrow arrow-down" viewBox="0 0 512.171 512.171">
            <path d="M479.046,283.925c-1.664-3.989-5.547-6.592-9.856-6.592H352.305V10.667C352.305,4.779,347.526,0,341.638,0H170.971
            c-5.888,0-10.667,4.779-10.667,10.667v266.667H42.971c-4.309,0-8.192,2.603-9.856,6.571c-1.643,3.989-0.747,8.576,2.304,11.627
            l212.8,213.504c2.005,2.005,4.715,3.136,7.552,3.136s5.547-1.131,7.552-3.115l213.419-213.504
            C479.793,292.501,480.71,287.915,479.046,283.925z"/>
          </svg>) the Train in the last {this.state.lastNSeconds} seconds.
        </div>
      </div>
    )
  }
}

function Cart(props) {
  return(
    <div className="cart">
      <div className="load">
        <img className="target" src="/assets/target.svg" type="image/svg+xml"></img>
        <div className="load-value">{props.n}<span>/{props.max}</span></div>
      </div>
      <div className="last-transfer">
        <div className="entered transfer-data">
          <svg className="arrow arrow-up" viewBox="0 0 512.171 512.171">
            <path d="M479.046,283.925c-1.664-3.989-5.547-6.592-9.856-6.592H352.305V10.667C352.305,4.779,347.526,0,341.638,0H170.971
            c-5.888,0-10.667,4.779-10.667,10.667v266.667H42.971c-4.309,0-8.192,2.603-9.856,6.571c-1.643,3.989-0.747,8.576,2.304,11.627
            l212.8,213.504c2.005,2.005,4.715,3.136,7.552,3.136s5.547-1.131,7.552-3.115l213.419-213.504
            C479.793,292.501,480.71,287.915,479.046,283.925z"/>
          </svg>
          <span>{props.entered}</span>
        </div>
        <div className="exited transfer-data">
          <svg className="arrow arrow-down" viewBox="0 0 512.171 512.171">
            <path d="M479.046,283.925c-1.664-3.989-5.547-6.592-9.856-6.592H352.305V10.667C352.305,4.779,347.526,0,341.638,0H170.971
            c-5.888,0-10.667,4.779-10.667,10.667v266.667H42.971c-4.309,0-8.192,2.603-9.856,6.571c-1.643,3.989-0.747,8.576,2.304,11.627
            l212.8,213.504c2.005,2.005,4.715,3.136,7.552,3.136s5.547-1.131,7.552-3.115l213.419-213.504
            C479.793,292.501,480.71,287.915,479.046,283.925z"/>
          </svg>
          <span>{props.exited}</span>
        </div>
      </div>
    </div>
)}

ReactDOM.render(<Dash />, document.getElementById("app"));