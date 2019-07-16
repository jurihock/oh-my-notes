{% macro setup() %}

  <script>

  require(['fontawesome']);

  require(['jquery', 'bootstrap'], function()
  {
    $(function()
    {
      // init tooltips
      $('[data-toggle="tooltip"]').tooltip();

      // clip text if too long
      $(document).on('mouseenter', '.clip', function()
      {
        // https://stackoverflow.com/a/13259660

        var $this = $(this);
        var $title = $this.attr('title');

        if (!$title)
        {
          if (this.offsetWidth < this.scrollWidth)
          {
            $this.attr('title', $this.text());
          }
        }
        else
        {
          if (this.offsetWidth >= this.scrollWidth && $title == $this.text())
          {
            $this.removeAttr('title');
          }
        }
      });
    });
  });

  require(['jquery', 'bootstrap', 'selectize'], function()
  {
    $(function()
    {
      $('#create_folder_dialog').on('show.bs.modal', function()
      {
        $('#create_folder_name').data('selectize').setValue('');
      });

      $('#create_folder_dialog').on('shown.bs.modal', function()
      {
        $('#create_folder_name').data('selectize').focus();
      });

      $('#create_file_dialog').on('show.bs.modal', function()
      {
        $('#create_file_folder').data('selectize').setValue('{{ selected.folder.name }}');
        $('#create_file_name').val('');
        $('#create_file_type_markdown').prop('checked', true);
        $('#create_file_type_lilypond').prop('checked', false);
      });

      $('#create_file_dialog').on('shown.bs.modal', function()
      {
        $('#create_file_name').focus();
      });

      for (let id of [ '#create_folder_name', '#create_file_folder' ])
      {
        $(id).selectize(
        {
          labelField: 'value',
          valueField: 'value',
          searchField: 'value',
          maxItems: 1,
          openOnFocus: false,
          closeAfterSelect: true,
          selectOnTab: true,
          create: true,
          persist: true,
          preload: true,
          load: function(query, callback)
          {
            $.ajax(
            {
              url: $(id).attr('data-url'),
              data: { q: query },
              dataType: 'json'
            })
            .done(function(data) { callback( data.map(value=>({value})) ); })
            .fail(function() { callback(); })
          }
        });
      }
    });
  });

  require(['jquery', 'mousetrap'], function()
  {
    $(function()
    {
      Mousetrap.bind('alt+m', function() { $('#create_folder_dialog').modal('show'); }, 'keyup');
      Mousetrap.bind('alt+n', function() { $('#create_file_dialog').modal('show'); }, 'keyup');
      Mousetrap.bind('alt+e', function() { hide_selected_file_preview(); }, 'keyup');
      Mousetrap.bind('alt+v', function() { show_selected_file_preview(); }, 'keyup');
    });
  });

  require(['jquery'], function()
  {
    $(function()
    {
      $('button[data-href]').on('click', function()
      {
        var href = $(this).attr('data-href');
        window.location.replace(href);
        return false;
      });
    });
  });

  require(['jquery'], function()
  {
    $(function()
    {
      hide_selected_file_preview();
    });
  });

  </script>

{% endmacro %}

{% macro functions() %}

  <script>

  function show_hidden_folders()
  {
    require(['jquery'], function()
    {
      $('#folders-complete').removeClass('hide');
      $('#folders-incomplete').addClass('hide');
    });
  }

  function show_hidden_files()
  {
    require(['jquery'], function()
    {
      $('#files-complete').removeClass('hide');
      $('#files-incomplete').addClass('hide');
    });
  }

  // https://stackoverflow.com/a/47934160
  function convert_base64_string_to_blob(base64string, mimetype)
  {
    var bytes = atob(base64string);
    var buffer = [];

    for (let offset = 0; offset < bytes.length; offset += 512)
    {
      var slice = bytes.slice(offset, offset + 512);
      var chars = new Array(slice.length);

      for (let i = 0; i < slice.length; i++)
      {
        chars[i] = slice.charCodeAt(i);
      }

      var array = new Uint8Array(chars);
      buffer.push(array);
    }

    var blob = new Blob(buffer, { type: mimetype });
    return blob;
  }

  function save_selected_file_value(callback)
  {
    require(['jquery', 'toastr'], function()
    {
      var form = $('#selected_file_form');
      var type = form.attr('method');
      var url = form.attr('action');
      var data = form.serialize();
      var timeout = 3000; // ms

      $('#selected_file_value').attr('disabled', true);
      $('#selected_file_form_submit_button').attr('disabled', true);

      $.ajax({ type: type, url: url, data: data, timeout: timeout })
      .done(function()
      {
        if (callback)
        {
          callback();
        }
        else
        {
          toastr.success('The file „{{ selected.folder.name }} / {{ selected.file.name }}“ was saved.', null, { timeOut: 1500 });
        }
      })
      .fail(function(jqxhr)
      {
        if (jqxhr.statusText == 'timeout')
        {
          toastr.error('Unable to save file „{{ selected.folder.name }} / {{ selected.file.name }}“ due to a timeout!', null);
        }
        else
        {
          toastr.error('Unable to save file „{{ selected.folder.name }} / {{ selected.file.name }}“ due to ' + jqxhr.responseText + '!', null);
        }
      })
      .always(function()
      {
        $('#selected_file_value').attr('disabled', false);
        $('#selected_file_form_submit_button').attr('disabled', false);
      });
    });
  }

  function show_selected_file_preview()
  {
    require(['jquery', 'toastr'], function()
    {
      var on_selected_file_preview_ready = function(data)
      {
        data = URL.createObjectURL(convert_base64_string_to_blob(data, 'application/pdf'));

        var args =
        {
          id: '{{ selected.file.id }}',
          fallbackLink:
          [
            '<p>',
            'It seems like your browser does not support online PDF viewing.',
            'Please download the <a href="' + secondaryUrl + '">PDF</a> to view it offline.',
            '</p>'
          ].join(' '),
          pdfOpenParams:
          {
            messages: 0,
            navpanes: 0,
            scrollbar: 0,
            statusbar: 0,
            toolbar: 0,
            view: 'FitH'
          }
        };

        $('#selected_file_preview').fadeOut(150, function()
        {
          $('#selected_file_preview').addClass('form-control');
          $('#selected_file_preview').html('');

          var pdf = PDFObject.embed(data, '#selected_file_preview', args);

          if (!pdf)
          {
            toastr.error('Unable to create preview for the file „{{ selected.folder.name }} / {{ selected.file.name }}“!', null);
          }

          $('#selected_file_preview').fadeIn(850);
        });
      };

      var on_selected_file_value_saved = function()
      {
        $('#selected_file_preview').html(
        [
          '<div class="center" style="width:50%">',
          '<div class="progress" style="height:1.5rem">',
          '<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%">Creating preview for the „{{ selected.folder.name }} / {{ selected.file.name }}“...</div>',
          '</div>',
          '</div>'
        ].join('\n'));

        $('#selected_file_edit_button_group').hide();
        $('#selected_file_preview_button_group').show();

        $('#selected_file_edit_button_group');
        $('#selected_file_preview_button_group');

        $('#selected_file_value').removeClass('size-hundred-percent').hide();
        $('#selected_file_preview').addClass('size-hundred-percent').fadeIn(250);

        var primaryUrl = '{{ url_for('preview_file', folder=selected.folder.id, file=selected.file.id) }}';
        var secondaryUrl = '{{ url_for('download_file', folder=selected.folder.id, file=selected.file.id, format='pdf') }}';

        $.ajax({ dataType: 'text', url: primaryUrl, timeout: 10000 })
        .done(function(data)
        {
          on_selected_file_preview_ready(data);
        })
        .fail(function(jqxhr)
        {
          if (jqxhr.statusText == 'timeout')
          {
            toastr.error('Unable to create preview for the file „{{ selected.folder.name }} / {{ selected.file.name }}“ due to a timeout!', null);
          }
          else
          {
            toastr.error('Unable to create preview for the file „{{ selected.folder.name }} / {{ selected.file.name }}“ due to ' + jqxhr.responseText + '!', null);
          }

          hide_selected_file_preview();
        });
      };

      save_selected_file_value(on_selected_file_value_saved);
    });
  }

  function hide_selected_file_preview()
  {
    require(['jquery'], function()
    {
      $('#selected_file_edit_button_group').show();
      $('#selected_file_preview_button_group').hide();

      $('#selected_file_preview').removeClass('size-hundred-percent').hide();
      $('#selected_file_value').addClass('size-hundred-percent').fadeIn(250);

      $('#selected_file_preview').removeClass('form-control');
      $('#selected_file_preview').html('');

      $('#selected_file_value').trigger('focus');
    });
  }

  </script>

{% endmacro %}
