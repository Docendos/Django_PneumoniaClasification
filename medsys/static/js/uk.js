django.jQuery(document).ready(function() {
    if (typeof django !== 'undefined') {
        django.jQuery.extend(django.jQuery.fn, {
            initFileField: function() {
                this.each(function() {
                    var $el = django.jQuery(this);
                    $el.find('input[type=file]').on('change', function() {
                        var fileName = '';
                        if (this.files && this.files.length > 1) {
                            fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
                        } else if (this.files && this.files.length == 1) {
                            fileName = this.files[0].name;
                        } else {
                            fileName = $el.attr('data-default-caption');
                        }
                        $el.find('.custom-file-label').text(fileName);
                    });
                });
            }
        });
        django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
            $row.find('.form-group').initFileField();
        });
    }
});
