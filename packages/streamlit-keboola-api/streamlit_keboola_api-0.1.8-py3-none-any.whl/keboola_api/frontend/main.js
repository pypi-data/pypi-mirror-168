
function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {
    const {label,key,api_only} = event.detail.args;
    if(api_only==true){
      if (!window.rendered) {
        sendValue(Math.random()*1000);
        Streamlit.setFrameHeight(0);
      }
    }
    else{
      document.getElementById("root").style.display='block'
      var upload = document.getElementById("upload");
      upload.textContent=label;
      upload.onclick = (event) =>{
        sendValue(Math.random()*1000)
      } 
    } 
    window.rendered = true 
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

Streamlit.setComponentReady()

Streamlit.setFrameHeight(50)
