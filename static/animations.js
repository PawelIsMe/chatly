function toggle() {
  var blur = document.getElementById('blur');
  var popup = document.getElementById('popup');
  console.log($('form')[0].checkValidity())

  //use on form
  if ($('form')[0].checkValidity()) {
    blur.classList.toggle('active');
    popup.classList.toggle('active');
  }
}
