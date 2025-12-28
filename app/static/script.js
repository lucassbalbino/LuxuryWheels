function openModal(){
   const modal = document.getElementById('modal-container')
   modal.classList.add('mostrar')

   modal.addEventListener('click', (e) =>{
       if (e.target.id == 'modal-container' || e.target.id == "fechar"){
           modal.classList.remove('mostrar')
           localStorage.fechaModal = 'modal-container'
       }
   })
}

btn.addEventListener('click', () => {
   const {id, marca, modelo, diaria, dias} = btn.dataset
   document.getElementById('modal-id').innerText = id
   document.getElementById('modal-marca').innerText = marca
   document.getElementById('modal-modelo').innerText = modelo
   document.getElementById('modal-diaria').innerText = diaria
   document.getElementById('modal-dias').innerText = dias
   openModal()
})