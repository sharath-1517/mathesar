<script lang="ts">
  import { _ } from 'svelte-i18n';

  import {
    iconDatabase,
    iconLogout,
    iconSettingsMajor,
    iconUser,
  } from '@mathesar/icons';
  import {
    ADMIN_URL,
    LOGOUT_URL,
    USER_PROFILE_URL,
    getDatabasePageUrl,
  } from '@mathesar/routes/urls';
  import { databasesStore } from '@mathesar/stores/databases';
  import { getReleaseDataStoreFromContext } from '@mathesar/stores/releases';
  import { getUserProfileStoreFromContext } from '@mathesar/stores/userProfile';
  import { preloadCommonData } from '@mathesar/utils/preloadData';
  import {
    DropdownMenu,
    Icon,
    LinkMenuItem,
    MenuDivider,
    MenuHeading,
  } from '@mathesar-component-library';

  import Breadcrumb from './breadcrumb/Breadcrumb.svelte';

  const commonData = preloadCommonData();
  const userProfile = getUserProfileStoreFromContext();
  const releaseDataStore = getReleaseDataStoreFromContext();
  const { currentDatabase } = databasesStore;

  $: database = $currentDatabase;
  $: upgradable = $releaseDataStore?.value?.upgradeStatus === 'upgradable';
  $: isNormalRoutingContext = commonData.routing_context === 'normal';
</script>

<header class="app-header">
  <div class="left">
    <Breadcrumb />
  </div>

  {#if isNormalRoutingContext}
    <div class="right">
      {#if $userProfile}
        <DropdownMenu
          triggerAppearance="ghost"
          size="small"
          closeOnInnerClick={true}
          menuStyle="--Menu__padding-x: 0.3em;"
        >
          <div class="user-switcher" slot="trigger">
            <Icon {...iconSettingsMajor} hasNotificationDot={upgradable} />
          </div>
          {#if database}
            <MenuHeading>{$_('database')}</MenuHeading>
            <LinkMenuItem
              icon={iconDatabase}
              href={getDatabasePageUrl(database.id)}
            >
              {database.name}
            </LinkMenuItem>
            <MenuDivider />
          {/if}
          <MenuHeading>{$_('signed_in_as')}</MenuHeading>
          <LinkMenuItem icon={iconUser} href={USER_PROFILE_URL}>
            {$userProfile.getDisplayName()}
          </LinkMenuItem>
          <MenuDivider />
          {#if $userProfile.isMathesarAdmin}
            <LinkMenuItem
              icon={iconSettingsMajor}
              href={ADMIN_URL}
              hasNotificationDot={upgradable}
            >
              {$_('administration')}
            </LinkMenuItem>
          {/if}
          <LinkMenuItem icon={iconLogout} href={LOGOUT_URL} tinro-ignore>
            {$_('log_out')}
          </LinkMenuItem>
        </DropdownMenu>
      {/if}
    </div>
  {/if}
</header>

<style lang="scss">
  .app-header {
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 1rem;
    height: var(--header-height, 60px);
    background-color: var(--slate-800);
    overflow: hidden;
    color: var(--white);
  }

  .left {
    display: flex;
    align-items: center;
    overflow: hidden;
  }

  .right {
    display: flex;
    align-items: center;
    font-size: var(--text-size-large);
  }

  .user-switcher {
    background-color: var(--slate-200);
    color: var(--slate-800);
    border-radius: var(--border-radius-m);
    padding: 0.5rem;
    display: flex;
    align-items: center;
  }
</style>
