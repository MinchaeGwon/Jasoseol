const targetForm = document.querySelector('.jss_content_form')
const counted_text = document.querySelector('.counted_text')

targetForm.addEventListener("keyup", function() {
    counted_text.innerHTML = "글자 수 : " + targetForm.value.length;
})
