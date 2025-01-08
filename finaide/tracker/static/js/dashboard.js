'use strict';
const show_wallet_btn = document.querySelector('.show-wallet');
const walletModal = document.querySelector('.wallet-modal');
const transModal = document.querySelector('.trans-modal');
const overlay = document.querySelector('.overlay');
const popupBtns = document.querySelectorAll('.toTop');









// ------------OPEN MODALS----------------------//
// open wallet modal
const openWalletModal = function () {
  // window.scrollTo({
  //   top: 0,
  //   behavior: "smooth" // Smooth scrolling
  // });
  walletModal.classList.remove('hidden');
  overlay.classList.remove('hidden');
};

// open transactional modal
const openTransModal = function () {
  transModal.classList.remove('hidden');
  overlay.classList.remove('hidden');
  // window.scrollTo({
  //   top: 0,
  //   behavior: "smooth" // Smooth scrolling
  // });
};


// Open edit transaction modal dynamically based on transaction ID
const openEditTransModal = function (transactionId) {
  const editTransModal = document.getElementById(`editTransactionModal${transactionId}`); // Find the correct modal by ID
  if (editTransModal) {
    editTransModal.classList.remove('hidden');
    overlay.classList.remove('hidden');
    // window.scrollTo({
    //   top: 0,
    //   behavior: "smooth" // Smooth scrolling
    // });
  }
};


// Open edit Wallet modal dynamically based on transaction ID
const openEditWalletModal = function (walletId) {
  const editWalletModal = document.getElementById(`editWalletModal${walletId}`); // Find the correct modal by ID
  if (editWalletModal) {
    editWalletModal.classList.remove('hidden');
    overlay.classList.remove('hidden');
    // window.scrollTo({
    //   top: 0,
    //   behavior: "smooth" // Smooth scrolling
    // });
  }
};

// ------------OPEN MODALS----------------------//


//-----------CLOSE MODALS---------------------///

const closeModal = function (){
  walletModal.classList.add('hidden');
  transModal.classList.add('hidden');
  overlay.classList.add('hidden');
}

// Open edit transaction modal dynamically based on transaction ID
const closeEditWalletModal = function (walletId) {
  const editWalletModal = document.getElementById(`editWalletModal${walletId}`); // Find the correct modal by ID
  if (editWalletModal) {
    
    editWalletModal.classList.add('hidden');
    overlay.classList.add('hidden');
    
  }

  
};

// Open edit transaction modal dynamically based on transaction ID
const closeEditTransModal = function (transactionId) {
  const editTransModal = document.getElementById(`editTransactionModal${transactionId}`); // Find the correct modal by ID
  if (editTransModal) {
    editTransModal.classList.add('hidden');
    overlay.classList.add('hidden');
   
  }
};

//-----------CLOSE MODALS---------------------///






// const closeModal = function () {
//   modal.classList.add('hidden');
//   overlay.classList.add('hidden');
// };

// for (let i = 0; i < btnsOpenModal.length; i++){
//   btnsOpenModal[i].addEventListener('click', openModal);

//   btnCloseModal.addEventListener('click', closeModal);
//   overlay.addEventListener('click', closeModal);

//   document.addEventListener('keydown', function (e) {
//     // console.log(e.key);

//   if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
//     closeModal();
//   }
// });
