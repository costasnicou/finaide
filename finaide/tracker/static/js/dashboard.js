const form_wallet = document.querySelector('.wallet_form');
const show_wallet_btn = document.querySelector('.show-wallet');
// function show_wallet(){


//     form_wallet.style.display = "block";

// }

// function hide_wallet(){


//     form_wallet.style.display = "block";

// }

'use strict';

const walletModal = document.querySelector('.wallet-modal');
const transModal = document.querySelector('.trans-modal');
const overlay = document.querySelector('.overlay');
// const btnOpenWalletModal = document.querySelector('.open-wallet-modal');
// const btnsOpenTransModal = document.querySelectorAll('.open-trans-modal');

const popupBtns = document.querySelectorAll('.toTop');


const openWalletModal = function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth" // Smooth scrolling
});
  walletModal.classList.remove('hidden');
  overlay.classList.remove('hidden');
};

const openTransModal = function () {
  transModal.classList.remove('hidden');
  overlay.classList.remove('hidden');
  window.scrollTo({
    top: 0,
    behavior: "smooth" // Smooth scrolling
});
};

const closeModal = function (){
  walletModal.classList.add('hidden');
  transModal.classList.add('hidden');
  overlay.classList.add('hidden');
}









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
