<template>
<v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <!-- <img src="@/assets/logo.png" alt="Vuetify.js" class="mb-5"> -->
        <div class="mb-20">
            <h1>{{ msg }} - {{port}}</h1>

             <v-container grid-list-md text-xs-center>
                <v-layout row wrap>
                    <v-flex xs4>
                        <v-btn color="success" v-on:click="onOpenSerial">打开串口</v-btn>
                    </v-flex>
                    <v-flex xs4>
                        <v-btn color="error" v-on:click="onStopSerial">关闭串口</v-btn>
                    </v-flex>
                </v-layout>
                <v-layout row wrap>
                    <v-flex  xs4 >
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>fast_rewind</v-icon>
                        </v-btn>
                    </v-flex>
                    <v-flex  xs4 >
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>keyboard_arrow_up</v-icon>
                        </v-btn>
                    </v-flex>
                    <v-flex  xs4 >
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>fast_forward</v-icon>
                        </v-btn>
                    </v-flex>
                </v-layout>
                <v-layout row wrap>
                    <v-flex  xs4 offset-xs0>
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>keyboard_arrow_left</v-icon>
                        </v-btn>
                    </v-flex>
                    <v-flex  xs4 offset-xs0>
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>stop</v-icon>
                        </v-btn>
                    </v-flex>
                    <v-flex  xs4 offset-xs0>
                        <v-btn fab dark large color="primary" v-on:click="onIconPress">
                            <v-icon dark>keyboard_arrow_right</v-icon>
                        </v-btn>
                    </v-flex>

                </v-layout>
                <v-layout row wrap>
                    <v-flex  xs4 offset-xs4>
                        <v-btn fab dark large color="primary"  v-on:click="onIconPress">
                            <v-icon dark>keyboard_arrow_down</v-icon>
                        </v-btn>
                    </v-flex>
                </v-layout>
            </v-container>
            <div class="text-xs-center">
                <v-btn fab dark large color="primary"  v-on:click="onCamera">
                    <v-icon dark>camera</v-icon>
                </v-btn>

                <v-btn fab dark large color="primary" v-on:click="onIconPress">
                    <v-icon dark>send</v-icon>
                </v-btn>
                <v-btn fab dark large color="primary" v-on:click="onIconPress">
                    <v-icon dark>refresh</v-icon>
                </v-btn>
            </div>
            <v-container grid-list-md text-xs-center>
                <div>
                    <v-btn dark fab color="cyan" value="A" v-on:click="onKeyPress">A</v-btn>
                    <v-btn dark fab color="cyan" value="B" v-on:click="onKeyPress">B</v-btn>
                    <v-btn dark fab color="cyan" value="C" v-on:click="onKeyPress">C</v-btn>
                </div>
  
                <div>
                    <v-btn dark fab color="teal" value="6" v-on:click="onKeyPress">抓</v-btn>
                    <v-btn dark fab color="teal" value="7" v-on:click="onKeyPress">举</v-btn>
                    <v-btn dark fab color="teal" value="8" v-on:click="onKeyPress">放</v-btn>
                </div>
            </v-container>
        </div>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
    
</template>

<script>
export default {
  name: "ControlPanel",
  props: {
    port: {
      type: String
    }
  },
  data() {
    return {
      msg: "Control Panel"
    };
  }, 
  mounted: function() {

    //   fetch("/api/v1/keys/mapping", { method: "GET" })
    //   .then(e => e.json())
    //   .then(data => {
    //     this.items.splice(data.length)
    //     for (let i = 0;i< data.length; i++){
    //       let ob = {
    //         icon: "bubble_chart",
    //         title: data[i]
    //       }
    //       this.$set(this.items, i, ob)
    //     }
    //   });
  }, 
  methods: {
      onOpenSerial:function() {
          fetch("/api/v1/serial/initial?port="+ this.port + "&baud_rate=9600", { method: "GET" })
          .then(s => s.json())
          .then((d) => {
              console.log(d)
          })
      },
      onStopSerial: function(){
          fetch("/api/v1/serial/close", { method: "GET" })
          .then(s => s.json())
          .then((d) => {
              console.log(d)
          })
      },
      onIconPress: function (event) {
          let target = event.currentTarget
          let key = target.querySelector("i").innerText
          fetch("/api/v1/serial/send?key=" + key , { method: "GET" })
          .then(s => s.json())
          .then((d) => {
              console.log(d)
          })
      }, 
      onKeyPress: function (event) {
          let target = event.currentTarget
          let data = target.getAttribute("value")
          fetch("/api/v1/serial/send?data=" + data , { method: "GET" })
          .then(s => s.json())
          .then((d) => {
              console.log(d)
          })
      }, 
      onCamera : function(event) {
          fetch("/api/v1/ocr/recognise", { method: "GET" })
      }
  }
};
</script>
