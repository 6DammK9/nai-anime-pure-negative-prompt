from cheesechaser.datapool import E621NewestWebpDataPool

pool = E621NewestWebpDataPool()
pool.batch_download_to_directory(
    resource_ids=[
        # older images, from NebulaeWis/e621-2024-webp-4Mpixel
        *range(1, 300),

        # newest images, from deepghs/e621_newest-webp-4Mpixel
        *range(5080000, 5080300),
    ],

    # save to directory /data/webp_e621
    dst_dir='/data/webp_e621',
)