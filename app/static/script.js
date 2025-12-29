function openModal(element){
   const modal = document.getElementById('modal-container')
   modal.classList.add('mostrar')
   
   if (element){
      const {id, marca, modelo, diaria, pagamentourl} = element.dataset
      // 2. Preenche as informações no Modal
      document.getElementById('modal-id').innerText = id
      document.getElementById('modal-marca').innerText = marca
      document.getElementById('modal-modelo').innerText = modelo
      document.getElementById('modal-diaria').innerText = diaria
   
      const btnReservar = document.getElementById('btn-reservar')
      if (btnReservar){
          btnReservar.href = pagamentourl  }
   }

   

   

   // 4. Configura o evento de fechar
   modal.addEventListener('click', (e) =>{
       if (e.target.id === 'modal-container' || e.target.id === "fechar-modal"){
           modal.classList.remove('mostrar')
           localStorage.fechaModal = 'modal-container'
       }
   })
}