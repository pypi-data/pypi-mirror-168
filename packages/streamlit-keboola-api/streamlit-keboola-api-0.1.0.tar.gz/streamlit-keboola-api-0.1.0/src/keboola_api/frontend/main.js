
function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {
  // if (!window.rendered) {
    const {label,key} = event.detail.args;
    var upload = document.getElementById("upload");
    upload.textContent=label;
    upload.onclick = (event) =>{
      sendValue(Math.random()*1000)
    } 
    window.rendered = true
  // }
  
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

Streamlit.setComponentReady()

Streamlit.setFrameHeight(50)
