/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                       */
/*  \   \        Copyright (c) 2003-2009 Xilinx, Inc.                */
/*  /   /          All Right Reserved.                                 */
/* /---/   /\                                                         */
/* \   \  /  \                                                      */
/*  \___\/\___\                                                    */
/***********************************************************************/

#include "xsi.h"

struct XSI_INFO xsi_info;



int main(int argc, char **argv)
{
    xsi_init_design(argc, argv);
    xsi_register_info(&xsi_info);

    xsi_register_min_prec_unit(-12);
    work_m_00000000001881958909_2281119288_init();
    work_m_00000000002289384195_0680589368_init();
    work_m_00000000001047641859_0001905836_init();
    work_m_00000000003278202829_2482856314_init();
    work_m_00000000002973426556_3383896982_init();
    work_m_00000000000398631876_2351635246_init();
    work_m_00000000001681872693_3723490554_init();
    work_m_00000000004134447467_2073120511_init();


    xsi_register_tops("work_m_00000000001681872693_3723490554");
    xsi_register_tops("work_m_00000000004134447467_2073120511");


    return xsi_run_simulation(argc, argv);

}
