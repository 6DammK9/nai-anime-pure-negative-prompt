#include "definations.h"

const char rtc0_hid[] = {
  0x53, 0x53, 0x44, 0x54, 0x59, 0x00, 0x00, 0x00, 0x02, 0x7f, 0x44, 0x49,
  0x58, 0x59, 0x45, 0x53, 0x52, 0x54, 0x43, 0x30, 0x5f, 0x48, 0x49, 0x44,
  0x00, 0x00, 0x00, 0x00, 0x49, 0x4e, 0x54, 0x4c, 0x28, 0x06, 0x23, 0x20,
  0xa0, 0x14, 0x00, 0x15, 0x5c, 0x2f, 0x03, 0x5f, 0x53, 0x42, 0x5f, 0x49,
  0x32, 0x43, 0x34, 0x52, 0x54, 0x43, 0x30, 0x06, 0x00, 0x10, 0x1f, 0x5c,
  0x2f, 0x03, 0x5f, 0x53, 0x42, 0x5f, 0x49, 0x32, 0x43, 0x34, 0x52, 0x54,
  0x43, 0x30, 0x08, 0x5f, 0x48, 0x49, 0x44, 0x0d, 0x44, 0x49, 0x58, 0x59,
  0x30, 0x30, 0x30, 0x30, 0x00
};

const char remove_ddrc[] = {
  0x53, 0x53, 0x44, 0x54, 0x65, 0x00, 0x00, 0x00, 0x02, 0x44, 0x44, 0x49,
  0x58, 0x59, 0x45, 0x53, 0x52, 0x45, 0x4d, 0x44, 0x44, 0x52, 0x43, 0x20,
  0x00, 0x00, 0x00, 0x00, 0x49, 0x4e, 0x54, 0x4c, 0x28, 0x06, 0x23, 0x20,
  0xa0, 0x1c, 0x00, 0x15, 0x5c, 0x2e, 0x5f, 0x53, 0x42, 0x5f, 0x44, 0x44,
  0x52, 0x32, 0x06, 0x00, 0x15, 0x5c, 0x2e, 0x5f, 0x53, 0x42, 0x5f, 0x44,
  0x44, 0x52, 0x33, 0x06, 0x00, 0x10, 0x11, 0x5c, 0x2e, 0x5f, 0x53, 0x42,
  0x5f, 0x44, 0x44, 0x52, 0x32, 0x08, 0x5f, 0x53, 0x54, 0x41, 0x00, 0x10,
  0x11, 0x5c, 0x2e, 0x5f, 0x53, 0x42, 0x5f, 0x44, 0x44, 0x52, 0x33, 0x08,
  0x5f, 0x53, 0x54, 0x41, 0x00
};

const char w510[] = {
  0x53, 0x53, 0x44, 0x54, 0xaa, 0x00, 0x00, 0x00, 0x02, 0xeb, 0x44, 0x49,
  0x58, 0x59, 0x45, 0x53, 0x44, 0x49, 0x58, 0x59, 0x45, 0x53, 0x30, 0x32,
  0x00, 0x00, 0x00, 0x00, 0x49, 0x4e, 0x54, 0x4c, 0x28, 0x06, 0x23, 0x20,
  0xa0, 0x33, 0x00, 0x15, 0x5c, 0x2f, 0x03, 0x5f, 0x53, 0x42, 0x5f, 0x49,
  0x32, 0x43, 0x30, 0x43, 0x4f, 0x4d, 0x31, 0x06, 0x00, 0x15, 0x5c, 0x2f,
  0x03, 0x5f, 0x53, 0x42, 0x5f, 0x53, 0x50, 0x49, 0x30, 0x43, 0x4f, 0x4d,
  0x32, 0x06, 0x00, 0x15, 0x5c, 0x2e, 0x5f, 0x53, 0x42, 0x5f, 0x57, 0x49,
  0x46, 0x49, 0x06, 0x00, 0x10, 0x1f, 0x5c, 0x2f, 0x03, 0x5f, 0x53, 0x42,
  0x5f, 0x49, 0x32, 0x43, 0x30, 0x43, 0x4f, 0x4d, 0x31, 0x08, 0x5f, 0x48,
  0x49, 0x44, 0x0d, 0x44, 0x49, 0x58, 0x59, 0x30, 0x30, 0x30, 0x31, 0x00,
  0x10, 0x1f, 0x5c, 0x2f, 0x03, 0x5f, 0x53, 0x42, 0x5f, 0x53, 0x50, 0x49,
  0x30, 0x43, 0x4f, 0x4d, 0x32, 0x08, 0x5f, 0x48, 0x49, 0x44, 0x0d, 0x44,
  0x49, 0x58, 0x59, 0x30, 0x30, 0x30, 0x32, 0x00, 0x10, 0x11, 0x5c, 0x2e,
  0x5f, 0x53, 0x42, 0x5f, 0x57, 0x49, 0x46, 0x49, 0x08, 0x5f, 0x53, 0x54,
  0x41, 0x00
};

int install_dbg2 (EFI_ACPI_TABLE_PROTOCOL *acpi_table) {
    uintn_t table_key;

    EFI_ACPI_DEBUG_PORT_2_TABLE Dbg2 = {
        {
            ARM_ACPI_HEADER(
                0x32474244 /*EFI_ACPI_6_1_DEBUG_PORT_2_TABLE_SIGNATURE, "DBG2" in le*/,
                EFI_ACPI_DEBUG_PORT_2_TABLE,
                0 /*EFI_ACPI_DEBUG_PORT_2_TABLE_REVISION*/
                ),
            offsetof(EFI_ACPI_DEBUG_PORT_2_TABLE, Ddi),
            NUMBER_DEBUG_DEVICE_INFO
        },
        {
            {
                {
                    0 /*EFI_ACPI_DBG2_DEBUG_DEVICE_INFORMATION_STRUCT_REVISION*/,
                    sizeof(EFI_ACPI_DBG2_DDI_STRUCT),
                    NUMBER_OF_GENERIC_ADDRESS,
                    NAMESPACE_STRING_SIZE,
                    offsetof(EFI_ACPI_DBG2_DDI_STRUCT, NamespaceString),
                    0,  //OemDataLength
                    0,  //OemDataOffset
                    EFI_ACPI_DBG2_PORT_TYPE_SERIAL,
                    EFI_ACPI_DBG2_PORT_SUBTYPE_SERIAL_ARM_PL011_UART,
                    {EFI_ACPI_RESERVED_BYTE, EFI_ACPI_RESERVED_BYTE},
                    offsetof(EFI_ACPI_DBG2_DDI_STRUCT, Address),
                    offsetof(EFI_ACPI_DBG2_DDI_STRUCT, AddressSize),
                },
                {
                    {
                    EFI_ACPI_6_1_SYSTEM_MEMORY,
                    32,
                    0,
                    EFI_ACPI_6_1_BYTE,
                    //0x400094080000/*FixedPcdGet64 (PcdSerialDbgRegisterBase)*/
                    0x94080000L/*FixedPcdGet64 (PcdSerialDbgRegisterBase)*/
                    }
                },
            {
                UART_LENGTH
            },
            NAMESPACE_STRING
            }
        }
    };

    efi_status_t ret = acpi_table->InstallAcpiTable(acpi_table, &Dbg2, sizeof(Dbg2), &table_key);
    if (EFI_SUCCESS != ret) {
        printf("failed InstallAcpiTable DBG2\n");
        return 1;
    }
    printf("DBG2 registered %d\n", table_key);

    return 0;
}

int install_spcr (EFI_ACPI_TABLE_PROTOCOL *acpi_table) {
    uintn_t table_key;
    
    EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE Spcr = {
        ARM_ACPI_HEADER ( 0x52435053 /* EFI_ACPI_6_2_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_SIGNATURE, "SPCR" in le */,
                        EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE,
                        0x02 /*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_REVISION*/),
        // UINT8                                   InterfaceType;
        0x03 /*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_INTERFACE_TYPE_ARM_PL011_UART*/,
        // UINT8                                   Reserved1[3];
        {
        EFI_ACPI_RESERVED_BYTE,
        EFI_ACPI_RESERVED_BYTE,
        EFI_ACPI_RESERVED_BYTE
        },
        // EFI_ACPI_6_2_GENERIC_ADDRESS_STRUCTURE  BaseAddress;
        { 0/*EFI_ACPI_5_0_SYSTEM_MEMORY*/, 32, 0, 3/*EFI_ACPI_5_0_DWORD*/, 0x94080000 }/*ARM_GAS32 (FixedPcdGet64 (PcdSerialRegisterBase))*/,
        // UINT8                                   InterruptType;
        0x8 /*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_INTERRUPT_TYPE_GIC*/,
        // UINT8                                   Irq;
        0,                                         // Not used on ARM
        // UINT32                                  GlobalSystemInterrupt;
        141,
        // UINT8                                   BaudRate;
        7/*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_BAUD_RATE_115200*/,
        // UINT8                                   Parity;
        0/*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_PARITY_NO_PARITY*/,
        // UINT8                                   StopBits;
        1/*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_STOP_BITS_1*/,
        // UINT8                                   FlowControl;
        0/*SPCR_FLOW_CONTROL_NONE*/,
        // UINT8                                   TerminalType;
        3 /*EFI_ACPI_SERIAL_PORT_CONSOLE_REDIRECTION_TABLE_TERMINAL_TYPE_ANSI*/,
        // UINT8                                   Reserved2;
        EFI_ACPI_RESERVED_BYTE,
        // UINT16                                  PciDeviceId;
        0xFFFF,
        // UINT16                                  PciVendorId;
        0xFFFF,
        // UINT8                                   PciBusNumber;
        0x00,
        // UINT8                                   PciDeviceNumber;
        0x00,
        // UINT8                                   PciFunctionNumber;
        0x00,
        // UINT32                                  PciFlags;
        0x00000000,
        // UINT8                                   PciSegment;
        0x00,
        // UINT32                                  Reserved3;
        EFI_ACPI_RESERVED_DWORD
    };

    efi_status_t ret = acpi_table->InstallAcpiTable(acpi_table, &Spcr, sizeof(Spcr), &table_key);
    if (EFI_SUCCESS != ret) {
        printf("failed InstallAcpiTable SPCR\n");
        return 1;
    }
    printf("SPCR registered %d\n", table_key);
    return 0;
}

int install_ssdt (EFI_ACPI_TABLE_PROTOCOL *acpi_table, const char *ssdt, size_t s) {
    uintn_t table_key;

    efi_status_t ret = acpi_table->InstallAcpiTable(acpi_table, (void *)ssdt, s, &table_key);
    if (EFI_SUCCESS != ret) {
        return 1;
    }
    return 0;
}

int uinstall_pcct(EFI_ACPI_TABLE_PROTOCOL *acpi_table, EFI_ACPI_SDT_PROTOCOL *acpi_sdt) {
    efi_status_t ret;
    EFI_ACPI_SDT_HEADER *pTable = NULL;
    EFI_ACPI_TABLE_VERSION dummy;
    uintn_t key;
    char sign[5] = { 0 };
    for (int i = 0; i < 256; i++) {
        ret = acpi_sdt->GetAcpiTable(i, &pTable, &dummy, &key);
        if (EFI_SUCCESS != ret) {
            printf("not found %d\n", i);
            break;
        }
        memcpy(sign, &pTable->Signature, 4);
        printf("found \"%s\" at %d\n", sign, i);

        if (pTable->Signature == 0x54434350 /* PCCT */) {
            printf("uninstall PCCT at %d\n", i);

            // pTable->Signature = 0x584d454f;
            
            ret = acpi_table->UninstallAcpiTable(acpi_table, key);
            if (EFI_SUCCESS != ret) {
                printf("failed UninstallAcpiTable PCCT\n");
                return 1;
            }
            break;
        }
    }
    return 0;
}

int set_fhd(efi_gop_t *gop) {
    efi_status_t ret;
    
    uint64_t max_pixels = 0;
    uintn_t isiz = sizeof(efi_gop_mode_info_t);
    efi_gop_mode_info_t *info = NULL;
    for (uintn_t try_mode = gop->Mode->MaxMode - 1; try_mode >= 0; try_mode--) {
        ret = gop->QueryMode(gop, try_mode, &isiz, &info);
        if (EFI_ERROR(ret) || info->PixelFormat > PixelBitMask) {
            // unsupported
            continue;
        }

        if (info->VerticalResolution * info->HorizontalResolution <= max_pixels){
            continue;
        }
        max_pixels = info->VerticalResolution * info->HorizontalResolution;

        printf("setting to %d: %dx%d\n", try_mode, info->HorizontalResolution, info->VerticalResolution);
        ret = gop->SetMode(gop, try_mode);
        if (EFI_ERROR(ret)) {
            fprintf(stderr, "unable to set video mode: %d\n", ret);
            return 1;
        }
        if (
            (info->HorizontalResolution == 3840 && info->VerticalResolution == 2160 ) ||
            (info->HorizontalResolution == 2560 && info->VerticalResolution == 1600 ) ||
            (info->HorizontalResolution == 2560 && info->VerticalResolution == 1440 ) ||
            (info->HorizontalResolution == 1920 && info->VerticalResolution == 1080 ) ||
            (info->HorizontalResolution == 1280 && info->VerticalResolution == 720 ) ||
            0
        ) {
            // prefered
            break;
        }
    }
    return 0;
}

int chainload_bootmgr() {
    efi_status_t ret;

    printf("chainload bootmgr\n");

    //"\\EFI\\Microsoft\\Boot\\cdboot_noprompt.efi",
    //"\\EFI\\Boot\\bootaa64-ms.efi"
    const char_t *try_paths[] = {
        "\\EFI\\Microsoft\\Boot\\bootmgfw.efi",
        "\\EFI\\Microsoft\\Boot\\cdboot_noprompt.efi",
        "\\EFI\\Microsoft\\Boot\\bootmgr.efi"
    };

    FILE *dummy;
    int i = 0;
    for (; try_paths[i] != NULL; i++) {
        dummy = fopen(try_paths[i], "*");
        if (dummy) {
            fclose(dummy);
            break;
        }
    }

    if (!dummy) {
        printf("failed to find bootmgfw.efi, cannot chainload\n");
        return 1;
    }

    efi_handle_t handle;
    wchar_t wpath[64];
    mbstowcs(wpath, try_paths[i], 64);

    const efi_guid_t dpftpGuid = EFI_DEVICE_PATH_FROM_TEXT_PROTOCOL_GUID;
    EFI_DEVICE_PATH_FROM_TEXT_PROTOCOL *dpftp;
    ret = BS->LocateProtocol((void*)&dpftpGuid, NULL, (void**)&dpftp);
    if (EFI_SUCCESS != ret) {
        printf("failed LocateProtocol EFI_DEVICE_PATH_FROM_TEXT_PROTOCOL: %d\n", ret);
        return 1;
    }

    const efi_guid_t dpttpGuid = EFI_DEVICE_PATH_TO_TEXT_PROTOCOL_GUID;
    EFI_DEVICE_PATH_TO_TEXT_PROTOCOL *dpttp;
    ret = BS->LocateProtocol((void*)&dpttpGuid, NULL, (void**)&dpttp);
    if (EFI_SUCCESS != ret) {
        printf("failed LocateProtocol EFI_DEVICE_PATH_TO_TEXT_PROTOCOL: %d\n", ret);
        return 1;
    }
    
    const efi_guid_t dpupGuid = EFI_DEVICE_PATH_UTILITIES_PROTOCOL_GUID;
    EFI_DEVICE_PATH_UTILITIES_PROTOCOL *dpup;
    ret = BS->LocateProtocol((void*)&dpupGuid, NULL, (void**)&dpup);
    if (EFI_SUCCESS != ret) {
        printf("failed LocateProtocol EFI_DEVICE_PATH_UTILITIES_PROTOCOL: %d\n", ret);
        return 1;
    }

    char buf[64];

    EFI_DEVICE_PATH_PROTOCOL *dev_node;
    const efi_guid_t dppGuid = EFI_DEVICE_PATH_PROTOCOL_GUID;
    ret = BS->OpenProtocol(
        LIP->DeviceHandle,
        (void *)&dppGuid,
        (void **)&dev_node,
        IM,
        NULL,
        EFI_OPEN_PROTOCOL_GET_PROTOCOL
    );
    if (EFI_SUCCESS != ret) {
        printf("failed OpenProtocol: %d\n", ret);
        return 1;
    }
    // wcstombs(buf, dpttp->ConvertDeviceNodeToText(dev_node, 0, 0), 64);
    // printf("cao %s\n", buf);

    EFI_DEVICE_PATH_PROTOCOL *dev_path = dpftp->ConvertTextToDevicePath(wpath);
    if (!dev_path) {
        printf("failed ConvertTextToDevicePath\n");
        return 1;
    }
    // wcstombs(buf, dpttp->ConvertDevicePathToText(dev_path, 0, 0), 64);
    // printf("cao2 %s\n", buf);

    dev_path = dpup->AppendDevicePath(dev_node, dev_path);
    if (!dev_path) {
        printf("failed AppendDevicePath\n");
        return 1;
    }
    wcstombs(buf, dpttp->ConvertDevicePathToText(dev_path, 0, 0), 64);
    printf("load %s\n", buf);

    ret = BS->LoadImage(0, IM, (void*)dev_path, NULL, 0, &handle);
    if (EFI_SUCCESS != ret) {
        printf("failed LoadImage %s: %d\n", try_paths[i], ret);
        return 1;
    }

    printf("start %s\n", try_paths[i]);
    ret = BS->StartImage(handle, NULL, NULL);
    if (EFI_SUCCESS != ret) {
        printf("failed StartImage %s: %d\n", try_paths[i], ret);
        return 1;
    }

    return 0;
}

// from util-linux
char *dmi_string(const EFI_SMBIOS_TABLE_HEADER *dm, uint8_t s)
{
	char *bp = (char *)dm;

	if (!s || !bp)
		return NULL;

	bp += dm->Length;
	while (s > 1 && *bp) {
		bp += strlen(bp);
		bp++;
		s--;
	}

	return !*bp ? NULL : bp;
}

const efi_guid_t acpi_guid = ACPI_TABLE_GUID;
const efi_guid_t acpi2_guid = ACPI_20_TABLE_GUID;
const efi_guid_t gop_guid = EFI_GRAPHICS_OUTPUT_PROTOCOL_GUID;
const efi_guid_t acpi_proto_guid = EFI_ACPI_TABLE_PROTOCOL_GUID;
const efi_guid_t acpi_sdt_guid = EFI_ACPI_SDT_PROTOCOL_GUID;
const efi_guid_t smbios_guid = EFI_SMBIOS_PROTOCOL_GUID;

#define white() ST->ConOut->SetAttribute(ST->ConOut, EFI_RED | EFI_GREEN | EFI_BLUE)
#define bright() ST->ConOut->SetAttribute(ST->ConOut, EFI_WHITE)
#define yellow() ST->ConOut->SetAttribute(ST->ConOut, EFI_YELLOW)
#define red() ST->ConOut->SetAttribute(ST->ConOut, EFI_RED | EFI_BRIGHT)
#define green() ST->ConOut->SetAttribute(ST->ConOut, EFI_GREEN | EFI_BRIGHT)
#define yprintf(fmt, ...) do {\
    yellow(); printf(fmt, ##__VA_ARGS__); white(); \
} while (0)
#define rprintf(fmt, ...) do {\
    red(); printf(fmt, ##__VA_ARGS__); white(); \
} while (0)
#define gprintf(fmt, ...) do {\
    green(); printf(fmt, ##__VA_ARGS__); white(); \
} while (0)
#define brprintf(fmt, ...) do {\
    bright(); printf(fmt, ##__VA_ARGS__); white(); \
} while (0)


int main(int argc, char **argv) {
    efi_status_t ret;
    efi_gop_t *gop = NULL;
    EFI_ACPI_TABLE_PROTOCOL *acpi_table = NULL;
    EFI_ACPI_SDT_PROTOCOL *acpi_sdt = NULL;
    EFI_SMBIOS_PROTOCOL *smbios = NULL;

    uint8_t cpus = 0; // up to 4 way?
    boolean_t has_pcct = 0;
    boolean_t has_spcr = 0;
    boolean_t has_dbg2 = 0;
    boolean_t is_w510 = 0;
    
    EFI_SMBIOS_HANDLE smbios_handle;
    EFI_SMBIOS_TYPE smbios_type;
    EFI_SMBIOS_TABLE_HEADER *smbios_table;
    const char *p_str;

    efi_configuration_table_t *p_table;
    EFI_ACPI_2_0_ROOT_SYSTEM_DESCRIPTION_POINTER *rsdp;
    EFI_ACPI_SDT_HEADER *xsdt, **sdt;

    ret = BS->LocateProtocol((void*)&gop_guid, NULL, (void**)&gop);
    if(EFI_ERROR(ret) || !gop) {
        fprintf(stderr, "failed LocateProtocol EFI_GRAPHICS_OUTPUT_PROTOCOL: %d\n", ret);
    } else {
        // this will clear console, so do at first
        if (!gop) {
            yprintf("Set Resolution: SKIPPED, cannot get GOP\n");
        } else {
            if (set_fhd(gop)) {
                rprintf("Set Resolution: FAILED\n");
            } else {
                gprintf("Set Resolution: OK\n");
            }
        }
    }

    // get EFI_SMBIOS_PROTOCOL
    ret = BS->LocateProtocol((void*)&smbios_guid, NULL, (void**)&smbios);
    if (EFI_SUCCESS != ret || NULL == smbios) {
        printf("failed LocateProtocol EFI_SMBIOS_PROTOCOL: %d\n", ret);
    } else {
        // get SMBIOS tables

        // type 0
        smbios_handle = 0xFFFE;
        smbios_type = 0;
        smbios_table = NULL;
        ret = smbios->GetNext(
            smbios,
            &smbios_handle,
            &smbios_type,
            &smbios_table,
            NULL
        );
        if (EFI_SUCCESS != ret || NULL == smbios_table) {
            printf("failed get dmi type 0: %d\n", ret);
        } else {
            p_str = dmi_string(smbios_table, ((SMBIOS_TABLE_TYPE0 *) smbios_table)->Vendor);
            printf("BIOS Vendor: %s\n", p_str);
            printf("BIOS Version: %s\n", dmi_string(smbios_table, ((SMBIOS_TABLE_TYPE0 *) smbios_table)->BiosVersion));
            printf("BIOS Release Date: %s\n", dmi_string(smbios_table, ((SMBIOS_TABLE_TYPE0 *) smbios_table)->BiosReleaseDate));
        }

        // type 1
        smbios_handle = 0xFFFE;
        smbios_type = 1;
        smbios_table = NULL;
        ret = smbios->GetNext(
            smbios,
            &smbios_handle,
            &smbios_type,
            &smbios_table,
            NULL
        );
        if (EFI_SUCCESS != ret || NULL == smbios_table) {
            printf("failed get dmi type 1: %d\n", ret);
        } else {
            printf("System Manufacturer: %s\n", dmi_string(smbios_table, ((SMBIOS_TABLE_TYPE1 *) smbios_table)->Manufacturer));
            p_str = dmi_string(smbios_table, ((SMBIOS_TABLE_TYPE1 *) smbios_table)->ProductName);
            printf("System Product Name: %s\n", p_str);
            //2251K + TK630: un.akeo.le + ACPI_BIOS_ERROR
            //2251K + PT620 (null): UEFI Shell OK
            if (p_str && (
                memmem(p_str, strlen(p_str), "TK630", 5) ||
                memmem(p_str, strlen(p_str), "W510", 4) ||
                memmem(p_str, strlen(p_str), "PGU-WBY0", 8)
            )) {
                is_w510 = 1;
            }
        }

        // type 4
        smbios_handle = 0xFFFE;
        smbios_type = 4;
        while (1) {
            smbios_table = NULL;
            ret = smbios->GetNext(
                smbios,
                &smbios_handle,
                &smbios_type,
                &smbios_table,
                NULL
            );
            if (smbios_handle == 0xFFFE) {
                break;
            }
            if (EFI_SUCCESS != ret || NULL == smbios_table) {
                printf("failed dmi type 4: %d\n", ret);
                break;
            } else {
                cpus++;
            }
        }
    }

    for (uintn_t i = 0; i < ST->NumberOfTableEntries; i++) {
        p_table = &ST->ConfigurationTable[i];
        if (
            memcmp(&p_table->VendorGuid, &acpi_guid, sizeof(acpi_guid)) &&
            memcmp(&p_table->VendorGuid, &acpi2_guid, sizeof(acpi2_guid))
        ) {
            //printf("not acpi %d\n", i);
            continue;
        }

        if (memcmp("RSD PTR ", (void *)(p_table->VendorTable), 8)) {
            continue;
        }

        rsdp = (void *)(p_table->VendorTable);
        printf("Version: %d  OEM ID: \"%s\"\n", (int)(rsdp->Revision), rsdp->OemId);
        if (rsdp->Revision < EFI_ACPI_2_0_ROOT_SYSTEM_DESCRIPTION_POINTER_REVISION) {
            printf("No XSDT table found.\n");
            continue;
        }

        xsdt = (void *)(rsdp->XsdtAddress);
        if (memcmp("XSDT", (char *)(&xsdt->Signature), 4)) {
            char bufSig[sizeof(xsdt->Signature) + 1] = {0};
            memcpy(bufSig, &xsdt->Signature, sizeof(xsdt->Signature));
            printf("ERROR: Invalid XSDT table found: \"%s\".\n", bufSig);
            continue;
        }

        sdt = (void*)&xsdt[1];
        for (uintn_t j = 0; j < (xsdt->Length - sizeof(*xsdt)) / 8; j++) {
            char bufSig[sizeof(sdt[0]->Signature) + 1] = {0};
            char bufOid[sizeof(sdt[0]->OemId) + 1] = {0};
            char bufOtid[sizeof(sdt[0]->OemTableId) + 1] = {0};
            memcpy(bufSig, &sdt[j]->Signature, sizeof(sdt[0]->Signature));
            memcpy(bufOid, sdt[j]->OemId, sizeof(sdt[0]->OemId));
            memcpy(bufOtid, sdt[j]->OemTableId, sizeof(sdt[0]->OemTableId));
            //printf("sign: \"%s\", oemid: \"%s\", oemtabid: \"%s\", version: %d\n", bufSig, bufOid, bufOtid, (uintn_t)sdt[j]->Revision);

            switch (sdt[j]->Signature) {
            case 0x54434350: /* PCCT */
                has_pcct = 1;
                break;
            case 0x32474244: /* DBG2 */
                has_dbg2 = 1;
                break;
            case 0x52435053: /* SPCR */
                has_spcr = 1;
                break;
            }
        }
    }

    // get EFI_ACPI_TABLE_PROTOCOL
    ret = BS->LocateProtocol((void*)&acpi_proto_guid, NULL, (void**)&acpi_table);
    if (EFI_SUCCESS != ret || NULL == acpi_table) {
        printf("failed LocateProtocol EFI_ACPI_TABLE_PROTOCOL: %d\n", ret);
    }

    // get EFI_ACPI_SDT_PROTOCOL
    ret = BS->LocateProtocol((void*)&acpi_sdt_guid, NULL, (void **)&acpi_sdt);
    if (EFI_SUCCESS != ret || NULL == acpi_sdt) {
        printf("failed LocateProtocol EFI_ACPI_SDT_PROTOCOL: %d\n", ret);
    }

    brprintf("Start patching\n");

    brprintf("(Windows) Uninstall PCCT\n");
    if (cpus > 1) {
        yprintf("SKIPPED, have more cpus: %d\n", cpus);
    } else if (!has_pcct) {
        yprintf("SKIPPED, not work for W510\n");
    } else if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else if (!acpi_sdt) {
        yprintf("SKIPPED, cannot get ACPI SDT Protocol\n");
    } else {
        if (uinstall_pcct(acpi_table, acpi_sdt)) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    brprintf("(Windows) Add DBG2\n");
    if (has_dbg2) {
        yprintf("SKIPPED, already have DBG2\n");
    } else if (is_w510) {
        yprintf("SKIPPED, not work for W510\n");
    } else if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else {
        if (install_dbg2(acpi_table)) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    brprintf("(Windows) Add SPCR\n");
    if (has_spcr) {
        yprintf("SKIPPED, already have SPCR\n");
    } else if (is_w510) {
        yprintf("SKIPPED, not work for W510\n");
    }  else if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else {
        if (install_dbg2(acpi_table)) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    brprintf("(Windows) Add _HID for RTC0\n");
    if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else {
        if (install_ssdt(acpi_table, rtc0_hid, sizeof(rtc0_hid))) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    brprintf("(Linux) Remove DDRC DDR2 DDR3\n");
    if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else {
        if (install_ssdt(acpi_table, remove_ddrc, sizeof(remove_ddrc))) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    brprintf("(Windows) W510 specific patch\n");
    if (!acpi_table) {
        yprintf("SKIPPED, cannot get ACPI Protocol\n");
    } else if (!is_w510) {
        yprintf("SKIPPED: not W510\n");
    } else {
        if (install_ssdt(acpi_table, w510, sizeof(w510))) {
            rprintf("FAILED\n");
        } else {
            gprintf("OK\n");
        }
    }

    // chainload
    if (argc == 0 || (argc > 1 && !strcmp(argv[1], "chainload"))) {
        // Synchronous Exception
        // Swap file and re-enter EFI 
        //chainload_bootmgr();
        printf("done\n");
    } else {
        printf("done\n");
    }

    return 0;
}
