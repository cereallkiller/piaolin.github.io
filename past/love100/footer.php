<?php if (!defined('__TYPECHO_ROOT_DIR__')) exit; ?>

<div class="container grid-sm s-content footer">
    <div class="column col-12">
        <p>内核：<a href="#" target="blank">Typecho</a>，模板：<a href="#" target="blank">LXY</a>，<a href="<?php $this->options->links(); ?>">ALBUM</a>。<a class="top" href="#">返回顶部</a></p>
    </div>
</div>
<?php $this->footer(); ?>

</body>
</html>
<?php if ($this->options->htmlCompress == 'enable'): $html_source = ob_get_contents(); ob_clean(); print htmlCompress($html_source); ob_end_flush(); endif; ?>