<?php
if (!defined('__TYPECHO_ROOT_DIR__')) exit;
$this->need('header.php');
?>

<div class="container grid-sm s-content posts">
	<div class="column col-12">
        <ol>
            <?php while($this->next()): ?>
            <li class=<?php if (array_key_exists('done',unserialize($this->___fields()))): ?>"done"<?php else : ?><?php endif; ?>><?php if (array_key_exists('done',unserialize($this->___fields()))): ?><del><?php $this->title() ?></del><?php else : ?><p><?php $this->title() ?></p><?php endif; ?></li>
            <?php endwhile; ?>
        </ol>
	</div>
</div>

<?php $this->need('footer.php'); ?>