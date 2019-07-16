require.config(
{
  shim:
  {
    'toastr': ['jquery'],
  },
  paths:
  {
    'toastr': 'assets/js/toastr/js/toastr-2.1.3.min',
  }
});

/*
require(['toastr', 'jquery'], function()
{
  $(function()
  {
    toastr.options =
    {
      positionClass: 'toast-top-right',
      timeOut: 3000
    };
  });
});
*/
